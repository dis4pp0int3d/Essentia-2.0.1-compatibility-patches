#!/usr/bin/env python3
"""Move Essentia 2.0.1 floating static constants out of class bodies for C++11."""

from pathlib import Path
import shutil
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: patch_essentia_2_0_1_cpp11.py <essentia-source-root>")
        return 2

    root = Path(sys.argv[1]).resolve()
    files = {
        "max_h": root / "src/algorithms/rhythm/tempotapmaxagreement.h",
        "max_cpp": root / "src/algorithms/rhythm/tempotapmaxagreement.cpp",
        "degara_h": root / "src/algorithms/rhythm/tempotapdegara.h",
        "degara_cpp": root / "src/algorithms/rhythm/tempotapdegara.cpp",
    }

    for path in files.values():
        if not path.is_file():
            print(f"Could not find expected Essentia source file: {path}")
            return 2

    updates = {key: path.read_text(encoding="utf-8") for key, path in files.items()}

    declarations = {
        "max_h": [
            (
                "  static const Real _minTickTime = 5.;  // ignore peaks before this time [s]",
                "  static const Real _minTickTime;  // ignore peaks before this time [s]",
            ),
            (
                "  static const Real _phaseThreshold = 0.175; // size of tolerance window for beat phase",
                "  static const Real _phaseThreshold; // size of tolerance window for beat phase",
            ),
            (
                "  static const Real _periodThreshold = 0.175; // size of tolerance window for beat period",
                "  static const Real _periodThreshold; // size of tolerance window for beat period",
            ),
        ],
        "degara_h": [
            (
                "  static const Real _frameDurationODF = 5.944308390022676;",
                "  static const Real _frameDurationODF;",
            ),
            (
                "  static const Real _alpha = 0.5; // decoding weighting parameter",
                "  static const Real _alpha; // decoding weighting parameter",
            ),
            (
                "  static const Real _sigma_ibi = 0.025; // std of the inter-beat interval pdf,",
                "  static const Real _sigma_ibi; // std of the inter-beat interval pdf,",
            ),
        ],
    }

    for key, pairs in declarations.items():
        for old, new in pairs:
            if old in updates[key]:
                updates[key] = updates[key].replace(old, new, 1)
            elif new not in updates[key]:
                print(f"Patch stopped: expected declaration not found in {files[key].name}.")
                return 1

    max_definitions = (
        "namespace essentia {\n"
        "namespace standard {\n"
        "const Real TempoTapMaxAgreement::_minTickTime = 5.;\n"
        "const Real TempoTapMaxAgreement::_phaseThreshold = 0.175;\n"
        "const Real TempoTapMaxAgreement::_periodThreshold = 0.175;\n"
        "}\n"
        "}\n\n"
    )
    max_anchor = "using namespace standard;\n\nconst char* TempoTapMaxAgreement::name"
    if "TempoTapMaxAgreement::_minTickTime =" not in updates["max_cpp"]:
        if max_anchor not in updates["max_cpp"]:
            print("Patch stopped: could not find the insertion point in tempotapmaxagreement.cpp.")
            return 1
        updates["max_cpp"] = updates["max_cpp"].replace(
            max_anchor,
            "using namespace standard;\n\n" + max_definitions + "const char* TempoTapMaxAgreement::name",
            1,
        )

    degara_definitions = (
        "const Real TempoTapDegara::_frameDurationODF = 5.944308390022676;\n"
        "const Real TempoTapDegara::_alpha = 0.5;\n"
        "const Real TempoTapDegara::_sigma_ibi = 0.025;\n\n"
    )
    degara_anchor = "namespace standard {\n\n\nconst char* TempoTapDegara::name"
    if "TempoTapDegara::_frameDurationODF =" not in updates["degara_cpp"]:
        if degara_anchor not in updates["degara_cpp"]:
            print("Patch stopped: could not find the insertion point in tempotapdegara.cpp.")
            return 1
        updates["degara_cpp"] = updates["degara_cpp"].replace(
            degara_anchor,
            "namespace standard {\n\n" + degara_definitions + "const char* TempoTapDegara::name",
            1,
        )

    changed = [key for key in files if updates[key] != files[key].read_text(encoding="utf-8")]
    if not changed:
        print("Essentia C++11 constants are already patched.")
        return 0

    for key in changed:
        path = files[key]
        backup = path.with_name(path.name + ".cpp11-backup")
        if not backup.exists():
            shutil.copy2(path, backup)
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(updates[key])

    print("Patched C++11 floating constants; original files saved with .cpp11-backup suffix.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
