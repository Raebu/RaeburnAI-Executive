import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root=process.cwd();
const workflowDir=path.join(root,'.github','workflows');
const sha40=/^[0-9a-f]{40}$/i;
const failures=[];
const usesPattern=/^\s*-?\s*uses:\s*([^\s#]+)(?:\s+#.*)?$/gm;

function read(p){
  const full=path.join(root,p);
  if(!fs.existsSync(full)){ failures.push(p+' is required'); return ''; }
  return fs.readFileSync(full,'utf8');
}
function requireMarker(source,file,label,marker){
  if(!source.includes(marker)) failures.push(file+' is missing '+label+': '+marker);
}

const workflowFiles=fs.readdirSync(workflowDir).filter(f=>/\.ya?ml$/.test(f)).sort();
const sources=new Map();
for(const wf of workflowFiles){
  const rel='.github/workflows/'+wf;
  const source=read(rel);
  sources.set(rel,source);
  usesPattern.lastIndex=0;
  for(const match of source.matchAll(usesPattern)){
    const ref=match[1];
    if(ref.startsWith('./')||ref.startsWith('docker://')) continue;
    const at=ref.lastIndexOf('@');
    const version=at>=0?ref.slice(at+1):'';
    if(!sha40.test(version)) failures.push(rel+' must pin third-party action to a 40-character commit SHA: '+ref);
  }
}

read('apps/api/requirements.lock');
read('apps/api/requirements-dev.lock');
read('apps/web/package-lock.json');

const ci=read('.github/workflows/ci.yml');
for(const marker of [
  'pip_audit -r apps/api/requirements.lock',
  '--require-hashes -r apps/api/requirements-dev.lock',
  'npm ci --ignore-scripts --no-audit',
  'npm audit --audit-level=high',
  'aquasecurity/trivy-action@',
  'raeburnai-executive-api:${{ github.sha }}',
  'raeburnai-executive-web:${{ github.sha }}',
  'http://127.0.0.1:8000/health',
  'http://127.0.0.1:3000/'
]) requireMarker(ci,'.github/workflows/ci.yml','required CI control',marker);

for(const dockerfile of ['Dockerfile.api','Dockerfile.web']){
  const source=read(dockerfile);
  if(!/^FROM\s+[^\s]+@sha256:[0-9a-f]{64}/m.test(source)) failures.push(dockerfile+' must pin its base by sha256 digest');
}
requireMarker(read('Dockerfile.api'),'Dockerfile.api','hash-locked dependency installation','--require-hashes -r requirements.lock');
requireMarker(read('Dockerfile.web'),'Dockerfile.web','deterministic npm installation','npm ci --ignore-scripts --no-audit');
requireMarker(read('docker-compose.yml'),'docker-compose.yml','digest-pinned Redis','redis:7-alpine@sha256:');

for(const legacy of ['.github/workflows/provenance.yml','.github/workflows/release-signing.yml']){
  if(fs.existsSync(path.join(root,legacy))) failures.push(legacy+' must be removed; release assets require one canonical owner');
}

const releasePath='.github/workflows/release-trust.yml';
const release=read(releasePath);
for(const marker of ['workflow_call:','git archive --format=tar','gzip -n','spdx-json','cyclonedx-json','SHA256SUMS','cosign sign-blob','cosign verify-blob','actions/attest@','gh attestation verify','gh release upload']){
  requireMarker(release,releasePath,'release trust control',marker);
}
const uploadCount=(release.match(/gh release upload/g)||[]).length;
if(uploadCount!==1) failures.push(releasePath+' must contain exactly one gh release upload command; found '+uploadCount);

const owners=[];
for(const [file,source] of sources.entries()){
  if(source.includes('gh release upload')||/upload-release-assets:\s*true/.test(source)) owners.push(file);
}
if(owners.length!==1||owners[0]!==releasePath) failures.push('release assets must have exactly one canonical workflow owner; found: '+(owners.join(', ')||'none'));

const sbom=read('.github/workflows/sbom.yml');
requireMarker(sbom,'.github/workflows/sbom.yml','repository-only release setting','upload-release-assets: false');
if(/\brelease:\s*\n\s*types:\s*\[published\]/.test(sbom)) failures.push('.github/workflows/sbom.yml must not own release-event packaging');

const policy=read('docs/software-supply-chain.md');
requireMarker(policy,'docs/software-supply-chain.md','Critical remediation expectation','**Critical:**');
requireMarker(policy,'docs/software-supply-chain.md','High remediation expectation','**High:**');
requireMarker(policy,'docs/software-supply-chain.md','real release evidence boundary','Real release evidence');

if(failures.length){
  console.error('Software supply-chain policy validation failed:');
  for(const failure of failures) console.error('- '+failure);
  process.exit(1);
}
console.warn('Software supply-chain policy validated: '+workflowFiles.length+' workflows use immutable action refs; dependency locks, image gates and a single release trust owner are present.');
