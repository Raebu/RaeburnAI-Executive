import sys

import atheris

with atheris.instrument_imports():
    from pydantic import ValidationError

    from raeburnai_executive.models import ActionExecutionRequest, BriefingRequest


def test_one_input(data: bytes) -> None:
    provider = atheris.FuzzedDataProvider(data)
    text = provider.ConsumeUnicodeNoSurrogates(4096)
    values = [part.strip() for part in text.split(",")[:12]]

    try:
        BriefingRequest(
            organisation=text[:160] or "RaeburnAI",
            executive_name=text[-160:] or "CEO",
            competitors=values[:10],
            focus_areas=values,
        )
    except ValidationError:
        pass

    try:
        ActionExecutionRequest(
            action_title=text[:300],
            target_system=text[-100:],
            dry_run=provider.ConsumeBool(),
        )
    except ValidationError:
        pass


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
