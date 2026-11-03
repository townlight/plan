import os

from townlight_planning.migrations import ready, source_engine, upgrade


def main():
    url = os.environ.get("TOWNLIGHT_PLANNING_POLICY_DB_URL")
    if not url:
        raise SystemExit("Set TOWNLIGHT_PLANNING_POLICY_DB_URL to the intended database; back it up before migration.")
    engine = source_engine(url)
    try:
        upgrade(engine)
        if not ready(engine):
            raise SystemExit("Planning migration readiness failed.")
        print("Planning schema townlight_planning_0002 ready; legacy records preserved.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
