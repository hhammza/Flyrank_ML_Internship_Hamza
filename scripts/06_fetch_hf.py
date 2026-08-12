import os
import re
import argparse
from huggingface_hub import hf_hub_download


def load_token_from_env(env_path=".env"):
    if not os.path.exists(env_path):
        return None
    token_keys = [
        "HUGGINGFACE_HUB_TOKEN",
        "HF_TOKEN",
        "HF_HUB_TOKEN",
        "HUGGINGFACE_TOKEN",
    ]
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # simple KEY=VALUE or KEY="VALUE"
            m = re.match(r"^([A-Za-z0-9_]+)\s*=\s*\"?(.*?)\"?$", line)
            if not m:
                continue
            k, v = m.group(1), m.group(2)
            if k in token_keys and v:
                return v
    return None


def main():
    parser = argparse.ArgumentParser(description="Download a file from the Hugging Face Hub using token in .env")
    parser.add_argument("repo_id", help="Repository id, e.g. 'username/repo' or 'dataset_name'")
    parser.add_argument("filename", help="Path to file inside the repo to download")
    parser.add_argument("--repo-type", choices=["model", "dataset", "space"], default=None, help="Repo type (optional)")
    parser.add_argument("--env", default=".env", help="Path to .env file to read token from")
    args = parser.parse_args()

    token = load_token_from_env(args.env)
    if token:
        os.environ["HUGGINGFACE_HUB_TOKEN"] = token
    else:
        print("No token found in", args.env)

    try:
        path = hf_hub_download(
            repo_id=args.repo_id,
            filename=args.filename,
            repo_type=args.repo_type,
            token=os.environ.get("HUGGINGFACE_HUB_TOKEN") or os.environ.get("HF_HOME")
        )
        print("Downloaded to:", path)
    except Exception as e:
        print("Download failed:", e)


if __name__ == "__main__":
    main()
