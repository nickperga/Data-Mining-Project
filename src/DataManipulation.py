import pandas as pd
import re

# Open the CSV file
df = pd.read_csv("save\data.csv", encoding="utf-8")

#Subtitutes the words of the pattern with null char
pattern = r"(Συνεδρίασε|ΣΥΝΕΔΡΙΑΣΕ|Με την παρουσία|Συνήλθε|ΣΥΝΗΛΘΕ)$"
df["judges"] = df["judges"].apply(lambda x: re.sub(pattern, "", x))

#Subtitutes the word of the pattern with null char
pattern = r"<< Επιστροφή"
df["final text"] = df["final text"].apply(lambda x: re.sub(pattern, "", x))

#Replaces the words of the replace with null char
df["judges"] = df["judges"].apply(lambda x: x.replace(", Αντιπρόεδρο του Αρείου Πάγου", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Αρεοπαγίτες", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", (σύμφωνα με την 2/2024 πράξη της Προέδρου του Αρείου Πάγου, κωλυομένης της Αντιπροέδρου Δήμητρας Ζώη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύουσα Αρεοπαγίτη (κωλυόμενης της Αντιπροέδρου Μαριάνθης Παγουτέλη),", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύουσα Αρεοπαγίτη (κωλυομένης της Αντιπροέδρου Μαριάνθης Παγουτέλη),", ""))
df["judges"] = df["judges"].apply(lambda x : x.replace(", (σύμφωνα με την 2/2024 πράξη της Προέδρου του Αρείου Πάγου,κωλυομένης της Αντιπροέδρου Δήμητρας Ζώη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Προεδρεύοντα Αρεοπαγίτη (σύμφωνα με την 2/2024 πράξη της Προέδρου του Αρείου Πάγου, κωλυομένης της Αντιπροέδρου Δήμητρας Ζώη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Προεδρεύοντα Αρεοπαγίτη (σύμφωνα με την 72/2024 πράξη της Προέδρου του Αρείου Πάγου, κωλυομένης της Αντιπροέδρου Δήμητρας Ζώη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη (σύμφωνα με την 72/2024 πράξη της Προέδρου του Αρείου Πάγου,κωλυομένης της Αντιπροέδρου Δήμητρας Ζώη),", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη (σύμφωνα με την ...2024 πράξη της Προέδρου του Αρείου Πάγου, κωλυομ ένης της Αντιπροέδρου Δήμητρας Ζώη),", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Αντιπροέδρο του Αρείου Πάγου", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Προεδρεύοντα Αντιπρόεδρο (σύμφωνα με την 187/2024 πράξη της Προέδρου του Αρείου Πάγου, κωλυομένης της Αντιπροέδρου Δήμητρας Ζώη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Προεδρεύοντα Αντιπρόεδρο (σύμφωνα με την ...2024 πράξη της Προέδρου του Αρείου Πάγου, κωλυομένης της Αντιπροέδρου Δήμητρας Ζώη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Προεδρεύοντα Αρεοπαγίτη (σύμφωνα με την 72/2024 πράξη της Προέδρου του Αρείου Πάγου, κωλυόμενης της Αντιπροέδρου Δήμητρας Ζώη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" - Εισηγήτρια", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" - Εισηγητή", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Προεδρεύουσα Αρεοπαγίτη", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Αντιπρόεδρο του ...,", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("-Εισηγητή", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", κωλυομένης της Αντιπροέδρου του Αρείου Πάγου Μαρίας Μουλιανιτάκη", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(κωλυομένης της Αντιπροέδρου Μαρίας Μουλιανιτάκη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", κωλυομένης της Αντιπροέδρου του Αρείου Πάγου Μ. Μουλιανιτάκη", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("- Εισηγήτρια", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("-Εισηγήτρια", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("-Εισηγήτρα", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Προεδρεύοντα Αρεοπαγίτη (λόγω κωλύματος της Αντιπρόεδρου Μυρσίνης Παπαχίου και της αρχαιοτέρας της συνθέσεως Αρεοπαγίτου Ασπασίας Μεσσηνιάτη - Γρυπάρη)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη (λόγω κωλύματος της Αντιπρόεδρου Μυρσίνης Παπαχίου και των αρχαιοτέρων της συνθέσεως Αρεοπαγιτών Ασπασίας Μεσσηνιάτη - Γρυπάρη και Σωκράτη Πλαστήρα),", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη (λόγω κωλύματος της Αντιπρόεδρου Μυρσίνης Παπα... και της αρχαιοτέρας της συνθέσεως Αρεοπαγίτου Ασπασίας Μεσσηνιάτη - Γρυπάρη),", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Αρεοπαγίτες", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη, (κωλυομένου του Αντιπροέδρου του Αρείου Πάγου Θεόδωρου Κανελλόπουλου),", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη, σύμφωνα με την υπ' αριθμ. 46/2024 Πράξη της Προέδρου του Αρείου Πάγου,", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη, σύμφωνα με την υπ' αριθμ. 46/2024 Πράξη της Προέδρου του Αρείου Πάγου και Εισηγητή,", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" - Εισηγήτια", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη,", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Αντιπρόεδρο Αρείου Πάγου", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Αντιπρόεδρο του Αρείου Πάγου", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Αντιπρόεδρο Αρείου του Πάγου,", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(σύμφωνα με την υπ' αρ. 383/2023 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(σύμφωνα με την υπ' αριθ. 53/2023 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύουσα Αρεοπαγίτη ", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(σύμφωνα με την υπ' αριθμ. 53/... πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(σύμφωνα με την υπ' αριθμ. 53/2023 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" (μετά την έκδοση της υπ' αρ. ...2024 απόφασης του Δικαστηρίου τούτου, με την οποία έγινε δεκτή η δήλωση αποχής την αρχικά ορισθείσης Εισηγήτριας Παρασκευής Τσούμαρη) ", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(σύμφωνα με την υπ' αριθ. 345/2022 πράξη της Προέδρου του Αρείου Πάγου) και Εισηγήτρια", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" (σύμφωνα με την υπ' αριθμ. ...2023 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(σύμφωνα με την υπ' αριθμ. 323/2023 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" Προεδερεύουσα Αρεοπαγίτη ,", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" Αντιπρόεδρος του Αρείου Πάγου", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(σύμφωνα με την υπ' αριθμ. 42/2022 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Προεδρεύοντα Αρεοπαγίτη (ως αρχαιότερο μέλος της συνθέσεως)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(",  (ως αρχαιότερο μέλος της συνθέσεως)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" (ως αρχαιότερο μέλος της συνθέσεως)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(" (η οποία ορίστηκε με την υπ'αριθμ. 56/2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ'αριθμ. 35/2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ'αριθμ. 97/2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ'αριθμ. 55/2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ' αριθμ. 97/2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ'αριθμ.97/2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ' αριθμ. 97/2024 Πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ.αρ. ...2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ'αριθ.97/2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("(η οποία ορίστηκε με την υπ αριθμ. 97/2024 πράξη της Προέδρου του Αρείου Πάγου)", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("- Εισηγητή", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Εισηγητή και", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace(", Προεδρεύοντα Αρεοπαγίτη και Εισηγητή", ""))
df["judges"] = df["judges"].apply(lambda x: x.replace("Εισηγητή,", ""))

df.to_csv("save\data.csv", index=False)