from sentence_transformers import SentenceTransformer

def download_and_save_model(model_name):
    model = SentenceTransformer(model_name)
    model.save(f"./apps/Model/{model_name}/")


if __name__ == "__main__":
    download_and_save_model("all-MiniLM-L6-v2")
