# import necessary packages
import pandas as pd

# pass the address
Address = "C:\\Users\TheAMG\Desktop\Ghorbani_Finance\Records"

# take the csv files and save them as Dataframes
Agas = pd.DataFrame(pd.read_csv(Address + "\Agas.csv"))
Agas = Agas[150::].reset_index(drop=True)
Agas = Agas[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Agas"})

Almas = pd.DataFrame(pd.read_csv(Address + "\Almas.csv"))
Almas = Almas[150::].reset_index(drop=True)
Almas = Almas[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Almas"})

Aminyekom = pd.DataFrame(pd.read_csv(Address + "\Aminyekom.csv"))
Aminyekom = Aminyekom[150::].reset_index(drop=True)
Aminyekom = Aminyekom[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Aminyekom"})

Asam = pd.DataFrame(pd.read_csv(Address + "\Asam.csv"))
Asam = Asam[150::].reset_index(drop=True)
Asam = Asam[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Asam"})

Asas = pd.DataFrame(pd.read_csv(Address + "\Asas.csv"))
Asas = Asas[150::].reset_index(drop=True)
Asas = Asas[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Asas"})

Atimes = pd.DataFrame(pd.read_csv(Address + "\Atimes.csv"))
Atimes = Atimes[150::].reset_index(drop=True)
Atimes = Atimes[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Atimes"})

Atlas = pd.DataFrame(pd.read_csv(Address + "\Atlas.csv"))
Atlas = Atlas[150::].reset_index(drop=True)
Atlas = Atlas[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Atlas"})

Bazr = pd.DataFrame(pd.read_csv(Address + "\Bazr.csv"))
Bazr = Bazr[::].reset_index(drop=True)
Bazr = Bazr[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Bazr"})

Firouze = pd.DataFrame(pd.read_csv(Address + "\Firouze.csv"))
Firouze = Firouze[150::].reset_index(drop=True)
Firouze = Firouze[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Firouze"})

Ofogmellat = pd.DataFrame(pd.read_csv(Address + "\Ofogmellat.csv"))
Ofogmellat = Ofogmellat[150::].reset_index(drop=True)
Ofogmellat = Ofogmellat[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Ofogmellat"})

Total = pd.merge(Agas, Almas, on="Date")
Total = pd.merge(Total, Aminyekom, on="Date")
Total = pd.merge(Total, Asam, on="Date")
Total = pd.merge(Total, Asas, on="Date")
Total = pd.merge(Total, Atimes, on="Date")
Total = pd.merge(Total, Atlas, on="Date")
Total = pd.merge(Total, Bazr, on="Date")
Total = pd.merge(Total, Firouze, on="Date")
Total = pd.merge(Total, Ofogmellat, on="Date")

Total.to_csv(Address + "\Total.csv")