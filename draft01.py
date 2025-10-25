# Clinical Expert System - Advanced Tree Version
# Course: CT-262 | Introduction to Artificial Intelligence
# Developer: Alizah Baig, Neha Salman
# Description: Rule-based decision tree for patient diagnosis

class Node:
    def __init__(self, question=None, yes=None, no=None, result=None):
        self.question = question
        self.yes = yes
        self.no = no
        self.result = result


# --- Final Outcomes (Leaf Nodes) ---
ambulance = Node(result="Call an ambulance immediately!")
doctor_flu = Node(result=" You might have flu or an infection. Visit the doctor.")
doctor_injury = Node(result=" You might have a physical injury. Consult the doctor.")
doctor_food = Node(result=" Possible food poisoning. Visit the doctor.")
doctor_migraine = Node(result=" You may have a migraine. Consult your doctor.")
doctor_dehydration = Node(result=" Possible dehydration. Drink fluids and visit doctor if persists.")
doctor_bp = Node(result=" Possible blood pressure issue. Visit the doctor soon.")
doctor_infection = Node(result=" Possible bacterial infection. Visit the doctor soon.")  # ✅ fixed missing node

home_allergy = Node(result=" Allergy detected. Avoid triggers and take antihistamines.")
home_cold = Node(result=" Common cold detected. Stay hydrated and rest well.")
home_fatigue = Node(result=" Fatigue detected. Sleep, rest, and maintain a healthy diet.")
fine = Node(result="No serious symptoms detected. You're fine for now!")


# --- Intermediate Symptom Nodes ---

# Breathing-related
breathing = Node("Do you have shortness of breath or chest pain?", yes=ambulance, no=doctor_flu)

# Fever path
sore_throat = Node("Do you have a sore throat or dry cough?", yes=breathing, no=home_cold)
body_ache = Node("Do you feel muscle pain or body ache?", yes=sore_throat, no=home_cold)

# Allergy path
itchy_eyes = Node("Do you have itchy eyes or runny nose?", yes=home_allergy, no=home_cold)
rashes = Node("Do you have skin rashes or redness?", yes=home_allergy, no=itchy_eyes)

# Stomach path
vomiting = Node("Are you vomiting or have diarrhea?", yes=doctor_food, no=doctor_injury)
stomach_pain = Node("Do you have stomach pain or cramps?", yes=vomiting, no=fine)

# Injury or infection path
injury = Node("Were you hit or injured recently?", yes=doctor_injury, no=stomach_pain)
infection = Node("Do you have burning sensation while urinating?", yes=doctor_infection, no=injury)

# Head-related
headache = Node("Do you have a severe headache?", yes=doctor_migraine, no=home_fatigue)
dizziness = Node("Do you feel dizzy or lightheaded?", yes=doctor_bp, no=headache)

# Dehydration and fatigue
thirst = Node("Are you feeling very thirsty and tired?", yes=doctor_dehydration, no=home_fatigue)
sleep = Node("Do you have trouble sleeping or feel exhausted?", yes=home_fatigue, no=fine)

# Flu or no fever path
flu = Node("Do you have flu-like symptoms (fever, cough, cold)?", yes=body_ache, no=rashes)

# Main fever check
fever = Node("Do you have a fever?", yes=flu, no=dizziness)

# Root of the tree
root = fever


# --- Helper Functions ---
def get_yes_no(question):
    while True:
        ans = input(question + " (yes/no): ").lower()
        if ans in ["yes", "no"]:
            return ans
        print("Please answer with 'yes' or 'no'.")


def traverse_tree(node, symptoms):
    if node.result:
        return node.result
    ans = get_yes_no(node.question)
    symptoms.append(f"{node.question} -> {ans}")
    return traverse_tree(node.yes if ans == "yes" else node.no, symptoms)


def save_to_file(name, age, gender, symptoms, recommendation):
    with open("patient_records.txt", "a") as f:
        f.write("=== Patient Record ===\n")
        f.write(f"Name: {name}\nAge: {age}\nGender: {gender}\n")
        f.write("Symptoms and Answers:\n")
        for s in symptoms:
            f.write("  - " + s + "\n")
        f.write(f"Final Recommendation: {recommendation}\n")
        f.write("=========================\n\n")


# --- Main System ---
def main():
    print("\n--- Clinical Expert System ---")
    name = input("Enter patient's name: ")
    age = input("Enter patient's age: ")
    gender = input("Enter patient's gender: ")

    print("\nPlease answer the following questions carefully.\n")
    symptoms = []
    recommendation = traverse_tree(root, symptoms)

    print("\n--- Diagnosis Result ---")
    print(recommendation)

    save_to_file(name, age, gender, symptoms, recommendation)
    print("\n✅ Patient record saved in 'patient_records.txt'.")
    print("--- End of Diagnosis ---")


if __name__ == "__main__":
    main()
