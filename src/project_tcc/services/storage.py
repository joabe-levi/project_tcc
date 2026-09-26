import json
import os


def salvar_json_no_volume(
    registro: dict,
    nome_arquivo: str,
) -> str:
    volume_path = os.getenv("FORMULARIOS_VOLUME")

    if not volume_path:
        raise RuntimeError(
            "Volume de formulários não configurado."
        )

    caminho_arquivo = os.path.join(
        volume_path,
        nome_arquivo,
    )

    with open(
        caminho_arquivo,
        "w",
        encoding="utf-8",
    ) as arquivo:
        json.dump(
            registro,
            arquivo,
            ensure_ascii=False,
            indent=2,
        )

    return caminho_arquivo
