#!/usr/bin/env python3
"""
GitHub Pull Shark Achievement Booster
Tool otomasi aman untuk membuka dan meningkatkan badge Pull Shark di GitHub.

Cara kerja:
- Membuat branch baru secara dinamis
- Menambahkan pembaruan catatan mikro pada file CHANGELOG.md
- Membuka Pull Request via GitHub CLI
- Melakukan auto-merge dan membersihkan branch
- Mengulang hingga target PR tercapai
"""

import os
import sys
import time
import subprocess
import argparse

def run_cmd(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode, proc.stdout.strip()

def check_requirements():
    code, _ = run_cmd(["git", "--version"])
    if code != 0:
        print("[ERROR] Git tidak terinstall!")
        sys.exit(1)

    code, out = run_cmd(["gh", "auth", "status"])
    if code != 0:
        print("[ERROR] GitHub CLI (gh) belum login! Jalankan 'gh auth login' terlebih dahulu.")
        sys.exit(1)

def get_current_merged_count(username: str) -> int:
    code, out = run_cmd(["gh", "api", f"search/issues?q=type:pr+is:merged+author:{username}", "--jq", ".total_count"])
    if code == 0 and out.isdigit():
        return int(out)
    return 0

def boost_pull_shark(target_count: int, delay: float = 2.0):
    print("=" * 60)
    print("GitHub Pull Shark Booster")
    print("=" * 60)

    # Dapatkan username aktif
    code, username = run_cmd(["gh", "api", "user", "--jq", ".login"])
    if code != 0 or not username:
        print("[ERROR] Gagal mendapatkan informasi akun GitHub!")
        sys.exit(1)

    current_merged = get_current_merged_count(username)
    print(f"[*] Akun GitHub : {username}")
    print(f"[*] Total PR Merged saat ini : {current_merged}")

    needed = max(0, target_count - current_merged)
    if needed == 0:
        print(f"[OK] Target ({target_count} PR) sudah tercapai atau terlampaui!")
        return

    print(f"[*] Target PR yang akan dibuat : {needed} PR (Menuju {target_count})")
    print("-" * 60)

    # Pastikan branch main up to date
    run_cmd(["git", "checkout", "main"])
    run_cmd(["git", "pull", "origin", "main"])

    changelog_file = "CHANGELOG.md"
    if not os.path.exists(changelog_file):
        with open(changelog_file, "w") as f:
            f.write("# Catatan Pembaruan Repositori\n\n")

    for i in range(1, needed + 1):
        branch_name = f"patch/pr-{current_merged + i}"
        print(f"\n[{i}/{needed}] Memproses PR #{current_merged + i} (Branch: {branch_name})...")

        # 1. Checkout new branch
        run_cmd(["git", "checkout", "-b", branch_name])

        # 2. Update changelog
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(changelog_file, "a") as f:
            f.write(f"- Pembaruan otomatis rilis #{current_merged + i} pada {timestamp} UTC\n")

        # 3. Commit
        run_cmd(["git", "add", changelog_file])
        c_code, _ = run_cmd(["git", "commit", "-m", f"chore: pembaruan catatan rilis #{current_merged + i}"])
        if c_code != 0:
            print("  [WARN] Tidak ada perubahan untuk di-commit.")
            run_cmd(["git", "checkout", "main"])
            run_cmd(["git", "branch", "-D", branch_name])
            continue

        # 4. Push branch
        p_code, p_out = run_cmd(["git", "push", "-u", "origin", branch_name])
        if p_code != 0:
            print(f"  [ERROR] Gagal push branch: {p_out}")
            run_cmd(["git", "checkout", "main"])
            run_cmd(["git", "branch", "-D", branch_name])
            continue

        # 5. Create Pull Request
        pr_title = f"chore: pembaruan catatan rilis #{current_merged + i}"
        pr_body = f"Pembaruan berkala untuk verifikasi alur integrasi pull request #{current_merged + i}."
        pr_code, pr_url = run_cmd(["gh", "pr", "create", "--title", pr_title, "--body", pr_body])
        if pr_code != 0:
            print(f"  [ERROR] Gagal membuat PR: {pr_url}")
            run_cmd(["git", "checkout", "main"])
            run_cmd(["git", "push", "origin", "--delete", branch_name])
            run_cmd(["git", "branch", "-D", branch_name])
            continue

        print(f"  [OK] PR dibuat: {pr_url}")

        # 6. Merge Pull Request
        m_code, m_out = run_cmd(["gh", "pr", "merge", branch_name, "--merge", "--delete-branch"])
        if m_code == 0:
            print(f"  [OK] PR #{current_merged + i} berhasil di-merge & branch dihapus.")
        else:
            print(f"  [WARN] Gagal auto-merge: {m_out}")

        # 7. Kembali ke main dan pull
        run_cmd(["git", "checkout", "main"])
        run_cmd(["git", "pull", "origin", "main"])

        # Delay santai agar aman dari API rate limit GitHub
        time.sleep(delay)

    final_merged = get_current_merged_count(username)
    print("\n" + "=" * 60)
    print(f"[OK] Selesai! Total PR Merged sekarang: {final_merged}")
    print("Periksa badge di: https://github.com/{username}?tab=achievements")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="GitHub Pull Shark Achievement Booster CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-t", "--target", type=int, default=16, help="Target total merged PR (16 untuk Silver, 128 untuk Gold)")
    parser.add_argument("-d", "--delay", type=float, default=2.0, help="Jeda waktu antar PR dalam detik")
    args = parser.parse_args()

    check_requirements()
    boost_pull_shark(args.target, args.delay)

if __name__ == "__main__":
    main()
