import os
import yt_dlp
from tqdm import tqdm


def main():
    # Запрашиваем ссылку на ролик
    video_url = input("Введите ссылку на ролик: ")

    # Функция для получения доступных форматов
    def get_formats():
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            available_formats = [
                {
                    "format_id": f["format_id"],
                    "resolution": f.get("resolution", "audio only"),
                    "ext": f["ext"],
                    "has_audio": not f.get("acodec") or f["acodec"] != "none",  # Улучшенная проверка
                    "audio_codec": f.get("acodec", "N/A"),
                    "video_codec": f.get("vcodec", "N/A")
                }
                for f in formats
            ]
            return info['title'], available_formats

    # Получаем список форматов
    try:
        video_title, formats = get_formats()
        print("\nДоступные качества:")
        for idx, f in enumerate(formats):
            audio_status = "Есть" if f["has_audio"] else "Нет"
            print(
                f"{idx + 1}. {f['resolution']} ({f['ext']}) | Видео: {f['video_codec']} | "
                f"Аудио: {f['audio_codec']} ({audio_status})"
            )
    except Exception as e:
        print(f"Ошибка получения форматов: {e}")
        return

    # Пользователь выбирает формат
    try:
        choice = int(input("\nВыберите качество (введите номер): "))
        selected_format = formats[choice - 1]['format_id']
    except (ValueError, IndexError):
        print("Неверный выбор!")
        return

    # Опции для скачивания
    output_dir = os.getcwd()  # Основная директория проекта
    ydl_opts = {
        'format': selected_format,
        'outtmpl': f"{output_dir}/{video_title}.%(ext)s",
        'progress_hooks': [tqdm_hook],
    }

    # Скачивание видео с прогресс-баром
    print(f"\nНачинаем скачивание: {video_title}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"\nСкачивание завершено: {video_title}")
    except Exception as e:
        print(f"Ошибка скачивания: {e}")


def tqdm_hook(d):
    """
    Хук для отображения прогресса скачивания через tqdm
    """
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d['downloaded_bytes']
        progress = downloaded_bytes / total_bytes if total_bytes else 0
        tqdm.write(f"Прогресс: {progress:.2%}", end="\r")
    elif d['status'] == 'finished':
        tqdm.write("\nСкачивание завершено.")


if __name__ == "__main__":
    main()