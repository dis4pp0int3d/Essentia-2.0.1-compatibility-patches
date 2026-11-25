# Essentia 2.0.1 compatibility patches

Two scripts for developers building the 2013 release of Essentia. One updates Python 2 print statements in the algorithm scanner for Python 3. The other moves floating-point constants in two tempo trackers from their class declarations to their C++ source files for C++11 compatibility.

## Apply the patches

Install Python 3. From the directory containing this README, get a clean copy of [Essentia v2.0.1](https://github.com/MTG/essentia/tree/v2.0.1) and run:

```sh
git clone --depth 1 --branch v2.0.1 https://github.com/MTG/essentia.git essentia-2.0.1
python3 patch_essentia_2_0_1_python3.py essentia-2.0.1
python3 patch_essentia_2_0_1_cpp11.py essentia-2.0.1
```

On Windows you can use `py -3` in place of `python3`. If you already have the source, skip the clone and pass the path to the folder containing `src` and `utils`.

Each script saves a backup beside every file it changes, using the suffix `.python2-backup` or `.cpp11-backup`. To undo a patch, copy the backups over the corresponding original filenames.

This package contains the patch scripts. Building the library itself requires the upstream build tools and dependencies. The patches address these two compatibility issues only.

## License

The scripts include excerpts from Essentia by the Music Technology Group, Universitat Pompeu Fabra. This patch distribution uses the GNU Affero General Public License, version 3 or later. The upstream notices and author credits are included in [licenses](licenses/). [License text](licenses/COPYING.txt)
