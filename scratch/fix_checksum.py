import json
import hashlib
import sys
from pathlib import Path

def compute_plugin_digest(metadata_file: Path, parser_file: Path) -> str:
    metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
    # Remove existing checksum/signature before hashing
    metadata.pop("checksum", None)
    metadata.pop("signature", None)
    metadata_canonical = json.dumps(metadata, sort_keys=True, separators=(",", ":"))
    metadata_digest = hashlib.sha256(metadata_canonical.encode("utf-8")).hexdigest()
    parser_digest = hashlib.sha256(parser_file.read_bytes()).hexdigest() if parser_file.exists() else ""
    return hashlib.sha256(f"{metadata_digest}:{parser_digest}".encode("utf-8")).hexdigest()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_checksum.py <plugin_dir>")
        sys.exit(1)
    
    plugin_dir = Path(sys.argv[1])
    metadata_file = plugin_dir / "metadata.json"
    parser_file = plugin_dir / "parser.py"
    
    if not metadata_file.exists():
        print(f"Error: {metadata_file} not found")
        sys.exit(1)
        
    print(compute_plugin_digest(metadata_file, parser_file))
