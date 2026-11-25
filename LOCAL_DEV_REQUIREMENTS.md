# Local Development Requirements (Outside GitHub)

This document lists everything required **beyond the files tracked on GitHub** to continue development, building, porting, and testing across every repository in `d:\Work\Projects\Wrench\GamePorting`.

---

## Summary Table

| Repository | Remote (`origin`) | Key Non-GitHub Requirements |
| --- | --- | --- |
| [`nx2android`](nx2android/) | `hosseinbannaei/nx2android` | Python 3.11+ + `pip` deps, downloaded tools (Android NDK, .NET SDK, `adb`), `keys/prod.keys`, game dumps (`.nsp`/`.xci`/`.nsz`/`.xcz`), Android device with USB debugging, generated build/data outputs |
| [`nx2androidX`](nx2androidX/) | `hosseinbannaei/nx2androidX` | Android SDK/NDK, JDK/Gradle, `gh` CLI (authenticated to fetch `NixPort/nixport-rootfs` payload), Python 3.11+ + `pip` deps, local `devtools/device.json` (if used), `keys/prod.keys` + game dumps on device/PC |
| [`repos/gal-guardians-android`](repos/gal-guardians-android/) | `hosseinbannaei/gal-guardians-android` | `keys/prod.keys`, *Gal Guardians: Demon Purge* (`0100B5301A180000`, `v262144`) dump, `fonttools` + local system bold font (for `extras/make_xbox_font.py`), and `nx2android` / `nx2androidX` |
| [`repos/octopath-traveler-android`](repos/octopath-traveler-android/) | `hosseinbannaei/octopath-traveler-android` | `keys/prod.keys`, *OCTOPATH TRAVELER* (`010057D006492000`, `v327680`) dump, and `nx2android` / `nx2androidX` |
| [`CozyDS/android`](CozyDS/android/) | `rafaelvcaetano/melonDS-android` (upstream) | Android SDK (`local.properties`), Android NDK/CMake/Gradle caches, `.nds` ROMs in `CozyDS/roms/` (and `CozyDS/pc-prototype/melonDS/` for PC testing) |

---

## 1. Shared Workspace Assets (Never Commit to GitHub)

These directories live alongside the repos in `d:\Work\Projects\Wrench\GamePorting\` and are intentionally kept out of GitHub:

- **`keys/`**
  - `prod.keys` and `title.keys` dumped from your own Nintendo Switch console.
  - Required by `nx2android` (`python -m porter port ... -k ...`) and `nx2androidX` (on-device extraction/porting).
- **`games/`**
  - Legally dumped Switch game files, extracted surveys/builds, and generated APKs/data packs:
    - `games/gal-guardians/`: `Gal Guardians Demon Purge [B+U262144].nsp`, `0100B5301A180000_build/`, `0100B5301A180000_survey/`, `GalGuardiansDemonPurge-data/`, `GalGuardiansDemonPurge.apk`, `backups/`, `extras/`
    - `games/octopath-traveler/`: `Octopath Traveler [010057D006492000][v0].nsp`, `Octopath Traveler [US][010057D006492800][v327680].nsp`, `010057D006492000_build/`, `OctopathTraveler-data/`, `OctopathTraveler.apk`, plus `AGENTS.md` (local device/testing notes)
- **`logs-archive/`**
  - Local `adb` logs (`device_log.txt`, `latest_log.txt`, `log_octopath.txt`, etc.), UI XML dumps (`ui.xml`, `popup.xml`), and device screenshots (`screen*.png`).
- **Signing Keystore**
  - Android APK signing keystore used by `nx2android` (`paths.signing_key()`) / Gradle release builds (never commit release keystores or passwords).
- **Optional Custom Vulkan Driver**
  - `libvulkan_freedreno.so` (Turnip) if testing custom Vulkan drivers on Qualcomm Adreno devices (`--vulkan-driver` / `porter driver`).

---

## 2. `nx2android` (`d:\Work\Projects\Wrench\GamePorting\nx2android`)

Fork of `shirai91/nx2android`. Active local branch: `work/local`.

### External Software & Toolchains
- **Python 3.11+** with packages from `requirements.txt`:
  - `lz4`, `capstone`, `pillow`, `fonttools`, `pyyaml`, `backports.zstd` (for Python < 3.14), `pycryptodome`, and `PySide6` (required for `python -m gui`; `python -m porter` CLI runs without `PySide6`).
- **Downloaded Porter Tools** (`python -m porter tools --download` or GUI **Setup → Download missing tools**):
  - Android NDK
  - .NET SDK
  - Android `adb` platform-tools
- **Disk Space**: ~30 GB free space for extraction, binary rewriting, shader translation, and output data packs.

### Local Data & Hardware
- `keys/prod.keys` (and `title.keys` if needed).
- Game dumps in `.nsp`, `.xci`, `.nsz`, or `.xcz` format (e.g., in `games/gal-guardians/` and `games/octopath-traveler/`).
- Physical Android device with **USB Debugging** enabled connected over `adb` (needed for `--install`, `porter driver`, `porter device_glslc`, and runtime testing).

---

## 3. `nx2androidX` (`d:\Work\Projects\Wrench\GamePorting\nx2androidX`)

Fork of `zFitness/nx2androidX` focused on the **APK-only, on-device** Android app (`android/` + `nxnative/dm/android/` + `porter/` + `phone_tools/`). Active local branch: `work/local`.

### External Software & Toolchains
- **Android SDK & NDK** + **JDK / Gradle** (for building the Android app in `android/` and compiling native host/shader code via `nxnative/dm/android/build.py`).
  - Note: `android/local.properties` is gitignored and must point `sdk.dir` to your local Android SDK if building from Android Studio/Gradle locally.
- **GitHub CLI (`gh`)** logged in:
  - Needed by `bash packaging/android-apk/build_apk.sh [debug|release]` to download the rootfs payload from the public `NixPort/nixport-rootfs` release (cached locally in `packaging/android-apk/.cache`, which is gitignored).
- **Python 3.11+** with `requirements.txt` (`lz4`, `capstone`, `pillow`, `fonttools`, `pyyaml`, `backports.zstd`, `pycryptodome`, `PySide6`).

### Local Config, Data & Hardware
- `devtools/device.json` (gitignored/local device target info used by `devtools/device.py` and `adb` workflows).
- Physical Android device with **USB Debugging** enabled over `adb`.
- On-device (or pushed) `prod.keys` and dumped Switch `.nsp`/`.xci`/`.nsz`/`.xcz` files for testing the in-app porting flow.
- *(CI-only, optional)* Repository secrets `QQBOT_APP_ID`, `QQBOT_APP_SECRET`, `QQBOT_GROUP_OPENID` for `devtools/qq_release_announce.py` (release announcements are `continue-on-error` and not needed for local builds).

---

## 4. `repos/gal-guardians-android` (`hosseinbannaei/gal-guardians-android`)

Documentation, testing notes, and helper script repo for *Gal Guardians: Demon Purge* (`0100B5301A180000`, `v262144`).

### External Requirements
- **Dumped Game + Keys**: Your own *Gal Guardians: Demon Purge* (`v262144`, base + update `1.1.0`) dump and `keys/prod.keys`.
- **Porting Toolchain**: Either `nx2android` (PC flow) or `nx2androidX` (on-device APK flow).
- **For `extras/make_xbox_font.py`**:
  - Python `fonttools` (`pip install fonttools`)
  - A local bold TrueType system font (defaults to `C:/Windows/Fonts/arialbd.ttf` on Windows, or pass a font path as the first argument) to generate `nintendo_ext_xbox.ttf` and `nintendo_ext_xbox_visual.ttf`.
- **Target Android Device**: Qualcomm Adreno (or Samsung Xclipse) recommended for hardware BC1–BC7 texture support; optional Turnip `libvulkan_freedreno.so`.

---

## 5. `repos/octopath-traveler-android` (`hosseinbannaei/octopath-traveler-android`)

Documentation and testing/thermal notes repo for *OCTOPATH TRAVELER* (`010057D006492000`, `v327680`).

### External Requirements
- **Dumped Game + Keys**: Your own *OCTOPATH TRAVELER* (`v327680`, base + update `1.0.5`) dump and `keys/prod.keys`.
- **Porting Toolchain**: Either `nx2android` (PC flow) or `nx2androidX` (on-device APK flow).
- **Target Android Device**: Qualcomm Adreno / Turnip (or Samsung Xclipse) recommended for hardware BC1–BC7 texture support and UE4.18 shaders (5,434 shaders); `adb` access for thermal/performance benchmarking.

---

## 6. `CozyDS/android` (`rafaelvcaetano/melonDS-android`)

Upstream `melonDS-android` checkout inside `CozyDS/`.

### External Requirements
- **Android SDK** configured in `CozyDS/android/local.properties` (currently `sdk.dir=C\:\\Users\\hosse\\AppData\\Local\\Android\\Sdk`, gitignored).
- **Android NDK / CMake / Gradle** (fetched/managed via Android Studio / Gradle wrapper `gradlew.bat` + `gradle/`).
- **Git Submodules** (`.gitmodules` — ensure submodules are initialized if building native `melonDS-android-lib` / `rcheevos-api`).
- **Nintendo DS ROMs** in `CozyDS/roms/` (gitignored/outside the repo; e.g., `4840 - Pokemon - SoulSilver Version (v10) (E).nds`).
- **PC Prototype Tools** (outside the `android/` git repo): `CozyDS/pc-prototype/melonDS/melonDS.exe` and `CozyDS/pc-prototype/index.html`.
- **Fork Remote (if pushing changes)**: `CozyDS/android` currently points `origin` to upstream `rafaelvcaetano/melonDS-android.git`; to push your own changes, add your own GitHub fork as a remote.
