import requests


def download_file_from_google_drive(file_id: str, destination: str) -> None:
    url = "https://docs.google.com/uc?export=download&confirm=t"

    session = requests.Session()

    response = session.get(url, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response) -> str:
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return ''


def save_response_content(response: requests.models.Response,
                          destination: str) -> None:
    chunk_size = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
