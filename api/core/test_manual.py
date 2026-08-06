"""
Script de prueba manual del extractor de paletas.

Cómo usarlo:
  1. Colocar imágenes de prueba en la carpeta core/test_images/
     (jpg, jpeg, png, webp o bmp)
  2. Desde la carpeta api/, correr:
     uv run python core/test_manual.py
"""

from pathlib import Path
from palette_extractor import extract_palette

TEST_IMAGES_DIR = Path(__file__).parent / "test_images"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def render_palette(image_name: str, palette: list[dict]) -> None:
    """Imprime la paleta en consola con una barra visual de porcentaje."""
    print(f"\n{'─' * 55}")
    print(f"  {image_name}")
    print(f"{'─' * 55}")
    for color in palette:
        bar_len = int(color["percentage"] / 2)
        bar = "█" * bar_len
        print(f"  {color['hex']}   {bar:<25}  {color['percentage']:5.1f}%  rgb{tuple(color['rgb'])}")


def main() -> None:
    if not TEST_IMAGES_DIR.exists():
        print(f"\n[!] Directorio no encontrado: {TEST_IMAGES_DIR}")
        print("    Crea la carpeta 'core/test_images/' y agrega algunas imágenes.")
        return

    images = sorted(
        f for f in TEST_IMAGES_DIR.iterdir()
        if f.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not images:
        print(f"\n[!] No se encontraron imágenes en {TEST_IMAGES_DIR}")
        print(f"    Formatos soportados: {', '.join(SUPPORTED_EXTENSIONS)}")
        return

    print(f"\nProcesando {len(images)} imagen(es) con 6 colores cada una...\n")
    errores = 0

    for image_path in images:
        try:
            palette = extract_palette(str(image_path), n_colors=6)
            render_palette(image_path.name, palette)
        except Exception as e:
            print(f"\n[ERROR] {image_path.name}: {e}")
            errores += 1

    print(f"\n{'─' * 55}")
    if errores == 0:
        print(f"  ✓ {len(images)} imagen(es) procesada(s) sin errores.")
    else:
        print(f"  ✗ {errores} error(es) de {len(images)} imagen(es).")


if __name__ == "__main__":
    main()
