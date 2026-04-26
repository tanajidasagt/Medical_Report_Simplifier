import pandas as pd
from datasets import load_dataset

def prepare_med_easi():
    # 1. Load the dataset
    print("Loading Med-EASi dataset...")
    dataset = load_dataset("Laitonjam/Med-EASi")
    
    # 2. Convert to Pandas for easy cleaning
    train_df = pd.DataFrame(dataset['train'])
    val_df = pd.DataFrame(dataset['validation'])
    
    # 3. Create the 'Prompt' format for Phi-2
    # We want the model to see: "Instruction: Simplify... Input: ... Output: ..."
    def format_phi2(row):
        return {
            "text": f"Instruction: Simplify the following medical text for a patient.\nInput: {row['Expert']}\nOutput: {row['Simple']}"
        }

    # Apply formatting
    formatted_train = train_df.apply(format_phi2, axis=1, result_type='expand')
    formatted_val = val_df.apply(format_phi2, axis=1, result_type='expand')

    # 4. Save to JSONL (standard format for fine-tuning)
    formatted_train.to_json("data/train_formatted.jsonl", orient="records", lines=True)
    formatted_val.to_json("data/val_formatted.jsonl", orient="records", lines=True)
    
    print(f"Done! Saved {len(formatted_train)} training samples to data/train_formatted.jsonl")

if __name__ == "__main__":
    prepare_med_easi()