import yt_dlp
import streamlit as st

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.ydl_opts = {'format': 'best'}
        self.video_info = None  # Información general del video
        self.selected_format = None  # Formato seleccionado para la descarga

    def fetch_info(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            self.video_info = ydl.extract_info(self.url, download=False)

    def showTitle(self):
        if self.video_info:
            st.write(f"Title: {self.video_info['title']}")
            self.showStreams()

    def showStreams(self):
        formats = self.video_info.get('formats', [])
        streams_options = [
            f"Resolucion: {format['height']}p / Tipo: {format['ext']} / Tamaño: {format.get('filesize', 'N/A')}"
            for format in formats if format.get('height')
        ]
        choice = st.selectbox("Select a stream", streams_options)
        self.selected_format = formats[streams_options.index(choice)]

    def getFileSize(self):
        file_size = self.selected_format.get('filesize', 0) / 1000000
        return file_size

    def getPermissionToContinue(self, file_size):
        st.write(f"**Titulo** {self.video_info['title']}")
        st.write(f"**Author** {self.video_info.get('uploader', 'N/A')}")
        st.write(f"**Tamaño** {file_size:.2f} MB")
        st.write(f"**Resolucion** {self.selected_format.get('height', 'N/A')}p")
        st.write(f"**Tipo** {self.selected_format.get('ext', 'N/A')}")

        if st.button("Descargar"):
            self.download()

    def download(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])
        st.success("Descarga completada")


if __name__ == "__main__":
    st.title("Descargador de video de YouTube")
    url = st.text_input("Insert the YouTube URL")
    if url:
        downloader = YouTubeDownloader(url)
        downloader.fetch_info()
        downloader.showTitle()
        if downloader.selected_format:
            file_size = downloader.getFileSize()
            downloader.getPermissionToContinue(file_size)
