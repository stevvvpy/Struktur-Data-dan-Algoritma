import pandas as pd
def read_data():
    sheet_id = '1hvHhvVt4hoXvf2x321Z0qai6COMDHSRw'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    return df

def read_data_connection():
    sheet_name = 'Relasi'
    sheet_id = '1hvHhvVt4hoXvf2x321Z0qai6COMDHSRw'
    df_pembobotan = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

    df = pd.read_csv(df_pembobotan)
    return df

# Membuat node
class node:
    def __init__(self, data):
        self.data = data    # Rolenya atau nama
        self.next = None    # Nama atau temannya
    
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
    
# Untuk data sheet 1    
def buat_linkedlist(df):
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

# Untuk data sheet 2
def sorting_data(df):
    df = df.sort_values(by=['Bobot'], ascending=True)
    return df

def encode_ke_nama(df_convert, df_teman):
    '''
    Mengubah ID nama sebagai dictionary dan menggconvertnya ke nama asli
    '''
    df_convert = df_convert.set_index('ID')['Nama'].to_dict()
    df_teman['Source'] = df_teman['Source'].map(df_convert)
    df_teman['Target'] = df_teman['Target'].map(df_convert)
    return df_teman

def buat_linkedlist_teman(df):
    '''
    Membuat linkedlist teman dengan 
    1. Menghapus kolom Relasi
    2. Menghapus kolom Skill
    3. Membuat dictionary dengan key sebagai source dan value sebagai Linkedlist
       Note: Value disusun berdasarkan bobot secara berurut
    '''
    df = sorting_data(df)
    # Menghapus kolom relasi dan skill
    if 'Relasi' in df.columns:
        df = df.drop(columns=['Relasi'])
    if 'Skill' in df.columns:
        df = df.drop(columns=['Skill'])
    
    # Membuat dictionary
    source_dict = {}

    for index, row in df.iterrows():
        source = row['Source']
        target = row['Target']

        # Jika Role belum pernah terdaftar di dictionary
        if source not in source_dict:
            source_dict[source] = Linkedlist()

        # Tambahkan nama
        source_dict[source].add(target+ " (" + str(row['Bobot']) + ")")

    return source_dict

# Fitur 1
def cari_role(data, target_role):
    target_role_clean = str(target_role).lower()
    
    role_ditemukan = None
    for key in data.keys():
        key_clean = str(key).lower().replace(" ", "")
        if key_clean in target_role_clean:
            role_ditemukan = key
            break

    if role_ditemukan:
        print(f"Role: {role_ditemukan}")
        print(f"Nama: ", end="")
        data[role_ditemukan].print()
        print("-" * 30)
    else:
        print(f"Role {target_role} tidak ditemukan.")

# Fitur 2
def print_nama_teman(data_teman):
    for nama, objek_list in data_teman.items():
        print(f"Nama dan teman berdasarkan bobot")
        print(f"Nama: {nama}")
        print("Teman: ", end="")
        objek_list.print()
        print("-" * 30)

# Fitur 3
def print_all(data):
    for role, objek_list in data.items():
        print(f"Role: {role}")
        objek_list.print()
        print("-" * 30)


# All Program
def main(data_linkedlist1, data_teman):
    print("Halo ! Okaeri !!!")
    print("==================")
    print("Apa keperluanmu?")
    print("1. Mencari role pekerjaan")
    print("2. Mencari nama teman")
    print("3. Menampilkan semua data")
    print("0. Keluar")
    
    pilihan = int(input("Masukkan pilihan: "))
    if pilihan == 1:
        print("Masukkan role pekerjaan: ")
        print("Role yang tersedia: " + ", ".join(data_linkedlist1.keys()))
        target_role = input()
        cari_role(data_linkedlist1, target_role)
        print("Tekan enter untuk kembali ke menu utama")
        input()
        
    if pilihan == 2:
        print_nama_teman(data_teman)
        print("Tekan enter untuk kembali ke menu utama")
        input()
    if pilihan == 3:
        print_all(data_linkedlist1)
        print("Tekan enter untuk kembali ke menu utama")
        input()
    if pilihan == 0:
        print("Terima kasih telah menggunakan program ini")
        exit()

if __name__ == "__main__":
    df_sheet_role = read_data()
    df_sheet_friend = read_data_connection()

    data_linkedlist1 = buat_linkedlist(df_sheet_role)
    data_teman = encode_ke_nama(df_sheet_role, df_sheet_friend)
    data_teman = buat_linkedlist_teman(df_sheet_friend)
    while True:
        main(data_linkedlist1, data_teman)