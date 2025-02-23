#!/usr/bin/python
#
#
# Written by Prima Agus Setiawan 
# a.k.a joeheartless / joefryme@gmail.com

import pandas as pd
import math
import openpyxl

print("HYDROGO HORTIKULTURA INDONESIA")
print("https://maps.app.goo.gl/NbkgKRvzLxKDK1s17")
print(50*"-")
def format_number(number):
    return f"{number:,}".replace(",", ".")

def format_rupiah(number):
    return f"{int(number):,}".replace(",", ".")

def kebutuhan_panen_harian(L, T, buffer):
    P = math.ceil(L / T) 
    P_prime = math.floor(P * (1 - buffer / 100))  
    return max(P_prime, 0) 

def total_lubang_tanam(P, T):
    return math.ceil(P * T)

def total_semai_harian(P, buffer):
    return math.ceil(P / (1 - buffer / 100))

def hitung_bobot_panen(P_prime, berat_per_tanaman):
    total_gram = P_prime * berat_per_tanaman  
    total_kg = total_gram / 1000 
    return round(total_kg, 2)

def hitung_pendapatan(bobot_panen_kg, harga_per_kg):
    pendapatan_harian = bobot_panen_kg * harga_per_kg
    pendapatan_bulanan = pendapatan_harian * 30
    pendapatan_tahunan = pendapatan_harian * 365
    return round(pendapatan_harian, 2), round(pendapatan_bulanan, 2), round(pendapatan_tahunan, 2)

def print_hasil_perhitungan(L, T, buffer, berat_per_tanaman, harga_per_kg, export_excel=False):
    P_prime = kebutuhan_panen_harian(L, T, buffer) 
    L_prime = total_lubang_tanam(P_prime, T) 
    S_prime = total_semai_harian(P_prime, buffer)
    bobot_panen_kg = hitung_bobot_panen(P_prime, berat_per_tanaman)
    pendapatan_harian, pendapatan_bulanan, pendapatan_tahunan = hitung_pendapatan(bobot_panen_kg, harga_per_kg)
    
    data = {
        "Parameter": [
            "Estimasi Panen Harian",
            "Estimasi Lubang Tanam Aktif",
            "Rotasi Semai Harian",
            "Estimasi Bobot Panen Harian",
            "Estimasi Pendapatan Harian",
            "Estimasi Pendapatan Bulanan",
            "Estimasi Pendapatan Tahunan"
        ],
        "Nilai": [
            format_number(P_prime),
            format_number(L_prime),
            format_number(S_prime),
            f"{bobot_panen_kg}",
            f"Rp {format_rupiah(pendapatan_harian)}",
            f"Rp {format_rupiah(pendapatan_bulanan)}",
            f"Rp {format_rupiah(pendapatan_tahunan)}"
        ],
        "Satuan": [
            "Tanaman/Hari",
            "Lubang Tanam",
            "Benih/Hari",
            "Kilogram/Hari",
            "Rupiah/Hari",
            "Rupiah/Bulan",
            "Rupiah/Tahun"
        ]
    }
    
    df = pd.DataFrame(data)
    print(df.to_string(index=False, justify="left"))

    
    if export_excel:
        df.to_excel("hasil_pola_tanam.xlsx", index=False)
        print("\nData berhasil diekspor ke hasil_pola_tanam.xlsx")

L = int(input("Masukkan total lubang tanam: "))
T = int(input("Masukkan waktu dari semai hingga panen (hari): "))
buffer = float(input("Masukkan buffer kegagalan dalam persen (misal 10 untuk 10%): "))
berat_per_tanaman = float(input("Masukkan berat rata-rata per tanaman (gram): "))
harga_per_kg = float(input("Masukkan harga jual per kg (Rp): "))
export_excel = input("Ingin mengekspor hasil ke Excel? (y/n): ").strip().lower() == 'y'

print_hasil_perhitungan(L, T, buffer, berat_per_tanaman, harga_per_kg, export_excel)
