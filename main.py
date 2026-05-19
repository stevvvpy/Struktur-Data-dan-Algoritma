import pandas as pd
def read_data():
    sheet_id = '1hvHhvVt4hoXvf2x321Z0qai6COMDHSRw'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    return df

# Membuat node
class node:
    def __init__(self, data):
        self.data = data    # Rolenya
        self.next = None    # Nama
    
class Linkedlist:
    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = node(data)
        if self.head is None:
            self.head = new_node
            return
        new_node.next = self.head
        self.head = new_node

    def print(self):
        temp = self.head
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")
    
def buat_linkedlist(df):
    if 'ID' in df.columns:
        df = df.drop(columns=['ID'])
    role_dict = {}

    for index, row in df.iterrows():
        nama = row['Nama']
        role = row['Role']

        # Jika Role belum pernah terdaftar di dictionary
        if role not in role_dict:
            role_dict[role] = Linkedlist()

        # Tambahkan nama
        role_dict[role].add(nama)

    return role_dict

def cari_role(role_dict, target_role):
    if target_role in role_dict:
        print(f"Role: {target_role}")
        print("Nama: ", end="")
        role_dict[target_role].print()
        print("-" * 30)
    else:
        print(f"Role {target_role} tidak ditemukan.")

def print_all(data):
    for role, objek_list in data.items():
        print(f"Role: {role}")
        objek_list.print()
        print("-" * 30)



def main():
    print("Halo ! Okaeri !!!")
    print("==================")
    print("Apa keperluanmu?")
    print("1. Mencari role pekerjaan")
    print("2. Mencari nama orang")
    print("3. Menampilkan semua data")
    print("0. Keluar")
    
    pilihan = int(input("Masukkan pilihan: "))
    if pilihan == 1:
        print("Masukkan role pekerjaan: ")
        target_role = input()
        df = read_data()
        cari_role(buat_linkedlist(df), target_role)
        print("Tekan enter untuk kembali ke menu utama")
        
    if pilihan == 2:
        print("Maaf fitur belum tersedia")
        print("Tekan enter untuk kembali ke menu utama")
        input()
    if pilihan == 3:
        df = read_data()
        role_dict = buat_linkedlist(df)
        print_all(role_dict)
        print("Tekan enter untuk kembali ke menu utama")
        input()
    if pilihan == 0:
        print("Terima kasih telah menggunakan program ini")
        exit()

if __name__ == "__main__":
    while True:
        main()