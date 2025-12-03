# examples/demo_classify.py
from alos_core.customs.engine import CustomsEngine

if __name__ == "__main__":
    engine = CustomsEngine()
    print("ALOS ANI demo. Type text (Ctrl+C to exit).")
    while True:
        try:
            txt = input("> ")
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        res = engine.predict_hs(txt)
        print(
            f"HS: {res['hs_code']} | conf={res['confidence']} | risk={res['risk_flag']} "
            f"| matched='{res['matched_desc']}' | norm='{res['normalized']}'"
        )
