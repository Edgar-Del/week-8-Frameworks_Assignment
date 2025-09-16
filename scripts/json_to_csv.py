import argparse
from pathlib import Path
import pandas as pd


def convert_json_to_csv(json_path: Path, csv_path: Path) -> None:
    # Tenta NDJSON (uma linha por objeto)
    try:
        df = pd.read_json(json_path, lines=True)
    except ValueError:
        # Tenta JSON padrão (lista de objetos)
        df = pd.read_json(json_path)

    # Salva CSV completo; sem índice
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Convert CORD-19 JSON (array ou NDJSON) para CSV")
    p.add_argument("--input", required=True, help="Caminho do JSON de metadados")
    p.add_argument("--output", required=True, help="Caminho de saída CSV")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    convert_json_to_csv(Path(args.input), Path(args.output))
    print(f"CSV salvo em: {args.output}")


if __name__ == "__main__":
    main()


