import os

from civicplan.migrations import ready, source_engine, upgrade


def main():
    url = os.environ.get("CIVICPLAN_POLICY_DB_URL")
    if not url:
        raise SystemExit("Set CIVICPLAN_POLICY_DB_URL to the intended database; back it up before migration.")
    engine = source_engine(url)
    try:
        upgrade(engine)
        if not ready(engine):
            raise SystemExit("Planning migration readiness failed.")
        print("Planning schema civicplan_0001 ready; legacy records preserved.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
