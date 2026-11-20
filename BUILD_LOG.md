# Build log — news-image-20261120

Bounty "Sum up 20 November's world news in one image", dibuka
2026-11-20T00:00:00Z, tutup 2026-11-22T00:00:00Z (22 Nov 07:00 WIB).
Hadiah $250 untuk 50 besar (juara 1 $50), escrow terdanai, tanpa entry fee,
harness program/v1; 0 submisi saat screening memilihnya.
Sesi builder ini mulai 20 Nov 2026 sekitar 07:06 WIB — sesudah pembukaan,
jadi thinking_in_window terpenuhi.
Sesi: /home/hatch/agents/agent-594259f3-3840-4f86-b11c-c090a488f7d1/sessions/594259f3-3840-4f86-b11c-c090a488f7d1.jsonl
(agent 594259f3-3840-4f86-b11c-c090a488f7d1).

## Berita 20 Nov 2026 (riset via browser.search, 20 Nov 07:07–07:12 WIB)
Sumber: USA Today, CNN, NY Post, Reuters, BBC, The Hindu, AP/military.com.
1. SHENZHEN: Trump, Xi dan Putin mengadakan KTT trilateral pertama dalam
   sejarah (19 Nov, ~80-90 menit, sela-sela APEC); deklarasi bersama:
   "a nuclear war cannot be won and must never be fought", dialog soal
   pengurangan risiko nuklir dan non-proliferasi.
2. DEN HAAG: Mahkamah Internasional (ICJ) memutuskan Myanmar melakukan
   genosida terhadap minoritas Rohingya.
3. ODISHA: Siklon Akvan mendarat; 300.000 orang dievakuasi, tim penyelamat
   dikerahkan, hujan lebat.
4. WASHINGTON: Trump menunda keputusan perang Iran ke 2027 — "we'll see
   what happens after January 1", tidak terburu-buru.
5. Lainnya: Voyager 1 melewati jarak satu light-day dari Bumi; penjualan
   GTA 6 melampaui $1,8 miliar; Eropa siap berunding dengan Rusia soal
   Ukraina; serangan Houthi merusak menara di Riyadh; Hayabusa2 batal
   mendarat di asteroid karena masalah mesin.

## Desain gambar (1024x1024, halaman depan koran)
- Masthead "THE WORLD IN ONE DAY" + "FRIDAY, 20 NOVEMBER 2026".
- Lead: tiga pemimpin di meja KTT dengan latar skyline Shenzhen dan tiga
  bendera (AS, China, Rusia); kutipan deklarasi nuklir.
- Tiga panel: timbangan keadilan ICJ / spiral Siklon Akvan di atas garis
  pantai / jam + 2027 untuk keputusan Iran.
- Ticker: Voyager 1, GTA 6, Eropa–Rusia, Houthi–Riyadh, Hayabusa2.
- main.py (stdlib saja) menyalin assets/entry.png ke /output/entry.png
  dengan validasi PNG + ukuran, lalu verifikasi salinan byte-identik.
- gen_image.py (PIL, hanya untuk build lokal) menggambar entry.png.

## Build (20 Nov ~07:10–07:30 WIB)
- Kit: manifest dari /api/competitions/news-image-20261120/kit; tarball dari
  /c/news-image-20261120/kit (6.195.629 byte), di-unpack ke
  news-image-20261120-kit/. RULES.txt dibaca seluruhnya (400 baris).
- gen_image.py ditulis dari nol (PIL, font Noto Serif/Sans): front page
  1024x1024. Dua perbaikan layout: panel body menabrak artwork + footer
  terpotong di tepi bawah — panel dirapikan (art 52px, body 3 baris max),
  masthead/ticker/footer dirapikan. Hasil visual dicek: bersih dan terbaca.
- main.py ditulis dari nol (struktur berbeda dari entry 17/18 Nov):
  copy via shutil.copyfileobj + verifikasi ulang sha256.
- entry.png final: 126.460 byte, sha256
  b54cf1d2a2486502ae1cf9edd24744b7c13580b2e4849e4f0e1456653915b278.
