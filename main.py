import argparse
import csv
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1 import CollectionReference

CRED_FILE = 'firebase-privateKey.json'


class Firestore:
    def __init__(self, cred_file: Path):
        cred = credentials.Certificate(cred_file)
        app = initialize_app(credential=cred)

        self.db = firestore.client(app=app)

    def get_collection(self, collection_name: str) -> CollectionReference:
        return self.db.collection(collection_name)

    def read_all(self, collection_name: str) -> list[dict]:
        collection = self.get_collection(collection_name)
        return [snapshot.to_dict() for snapshot in collection.get()]

    def get_all_collections(self) -> list[str]:
        return [collection.id for collection in self.db.collections()]

    def get_all_properties(self, collection_name: str) -> list[str]:
        collection = self.get_collection(collection_name)
        documents = collection.stream()
        all_properties = set()

        for doc in documents:
            doc_dict = doc.to_dict()
            all_properties.update(doc_dict.keys())

        return list(all_properties)


def process_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='firestore2csv')
    parser.add_argument('--cred-file', type=str, help='Path to the Firebase private key file', default=CRED_FILE)
    parser.add_argument('--exclude', type=str, help='Comma separated list of collections to exclude', default="")
    parser.add_argument('--output-dir', type=str, help='Path to the output directory', default='backups')

    return parser.parse_args()


def main(cred_file: str, exclude: str, output_dir: str):
    firestore_client = Firestore(Path(cred_file))

    backup_files = list()
    collections = firestore_client.get_all_collections()
    filtered_collections = list([collection for collection in collections if collection not in exclude.split(',')])

    with tempfile.TemporaryDirectory() as tempdir:
        for collection in filtered_collections:
            csv_file_path = process_collection(
                firestore_client,
                Path(f"{tempdir}/{collection}.csv"),
                collection
            )
            backup_files.append(csv_file_path)

        create_backup(backup_files, output_dir)


def process_collection(client: Firestore, file_path: Path, collection_name: str) -> Path:
    fields = client.get_all_properties(collection_name)
    docs = client.read_all(collection_name)

    with open(file_path, 'w') as csv_file:
        writer = csv_writer(csv_file, fields)
        writer.writeheader()

        for doc in docs:
            writer.writerow(doc)

        print(f'Wrote {len(docs)} documents to CSV from collection "{collection_name}"')

    return Path(file_path)


def csv_writer(file, fields: list[str]) -> csv.DictWriter:
    return csv.DictWriter(file, fieldnames=fields)


def create_backup(backup_files: list[Path], output_dir: str):
    backup_folder = Path(output_dir)
    backup_folder.mkdir(exist_ok=True)

    tar_file_path = Path(f"{backup_folder}/backup_{datetime.now()}.tar.gz")

    with tarfile.open(tar_file_path, 'w:gz') as tar_file:
        for file in backup_files:
            archive_name = file.name
            tar_file.add(file, arcname=archive_name)


if __name__ == '__main__':
    args = process_arguments()

    main(args.cred_file, args.exclude, args.output_dir)
