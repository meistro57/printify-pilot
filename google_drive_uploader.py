import os
import json
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import config

# Authenticate with Google Drive API
creds = google.auth.load_credentials_from_file(config.GOOGLE_SERVICE_ACCOUNT, scopes=["https://www.googleapis.com/auth/drive.file"])[0]
drive_service = build("drive", "v3", credentials=creds)

# Google Drive folder ID from config.py
FOLDER_ID = config.GOOGLE_DRIVE_FOLDER_ID

def upload_to_drive(file_path):
    """Uploads an image to Google Drive and saves the public URL."""
    file_name = os.path.basename(file_path)

    # Upload file
    file_metadata = {"name": file_name, "parents": [FOLDER_ID]}
    media = MediaFileUpload(file_path, mimetype="image/png")
    uploaded_file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()

    # Make file publicly accessible
    drive_service.permissions().create(
        fileId=uploaded_file["id"], body={"role": "reader", "type": "anyone"}
    ).execute()

    # Generate public link
    file_url = f"https://drive.google.com/uc?id={uploaded_file['id']}"
    print(f"✅ Uploaded Successfully: {file_url}")

    # **NEW: Save the URL to a file**
    with open("google_drive_image_url.txt", "w", encoding="utf-8") as f:
        f.write(file_url)

    print("📂 Image URL saved to google_drive_image_url.txt")
    return file_url

# Run uploader
def main():
    image_folder = "generated_images"
    images = sorted(
        [f for f in os.listdir(image_folder) if f.endswith(".png")],
        key=lambda x: os.path.getmtime(os.path.join(image_folder, x)),
        reverse=True,
    )

    if images:
        latest_image_path = os.path.join(image_folder, images[0])
        upload_to_drive(latest_image_path)
    else:
        print("❌ No image found for upload.")


if __name__ == "__main__":
    main()
