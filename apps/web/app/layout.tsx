import './styles.css';

export const metadata = {
  title: 'RaeburnAI Executive',
  description: "A CEO's second brain for daily briefings and decision support.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
