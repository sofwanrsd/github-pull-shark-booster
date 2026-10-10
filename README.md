# GitHub Pull Shark Booster

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![CLI: GitHub_CLI](https://img.shields.io/badge/CLI-GitHub_CLI-181717.svg?logo=github&logoColor=white)](https://cli.github.com/)

Tool otomasi ringan dan aman untuk membuka serta meningkatkan level badge resmi **Pull Shark** pada profil GitHub.

---

## Kasta Badge Pull Shark

| Tingkat | Syarat Merged PR | Tampilan Badge |
|---|---|---|
| Bronze (Default) | 2 PR | Badge Hiu Perunggu |
| Silver (x2) | 16 PR | Badge Hiu Perak |
| Gold (x3) | 128 PR | Badge Hiu Emas |

---

## Prasyarat

- Git terpasang di sistem.
- GitHub CLI (`gh`) terpasang dan sudah terautentikasi (`gh auth login`).
- Python 3.10+.

---

## Panduan Penggunaan

1. **Clone Repositori:**
   ```bash
   git clone https://github.com/sofwanrsd/github-pull-shark-booster.git
   cd github-pull-shark-booster
   ```

2. **Jalankan Booster (Target Silver - 16 PR):**
   ```bash
   python3 pull_shark_booster.py --target 16
   ```

3. **Jalankan Booster (Target Gold - 128 PR):**
   ```bash
   python3 pull_shark_booster.py --target 128 --delay 1.5
   ```

---

## Parameter CLI

| Parameter | Default | Keterangan |
|---|---|---|
| `-t, --target` | `16` | Target total merged PR yang ingin dicapai |
| `-d, --delay` | `2.0` | Jeda waktu dalam detik antar pembuatan PR |

---

## Lisensi

Proyek ini dilisensikan di bawah lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lengkap.
