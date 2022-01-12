
# KOCAELİ ÜNİVERSİTESİ YAZILIM LABORATUVARI (2021-2022) 

<details>
<summary>Kargo Dağıtım Sistemi</summary>

Bu projede bizden masaüstü kurye uygulaması istenmiştir. Kullanıcı, harita üzerinden yeni konumlar ekleyebilmektedir. Seçilen başlangıç konumundan başlayıp, tüm konumları gezecek şekilde tercih edilen algoritmaya göre rota çizdirilmektedir. Arayüz üzerinde HTML ve CSS kullanılabildiği için **electron.js** kütüphanesini tercih ettik. En kısa yolu bulmak için permütasyon ile tüm olası yollar arasından en kısa yolu seçtirdik. Detaylı bilgi için [tıklayınız](https://github.com/ertrldtcu/YazLab/blob/master/I/I/proje1.pdf).

**Ekran Görüntüleri**
![giriş ekranı](https://github.com/ertrldtcu/YazLab/blob/master/I/I/screenshots/login.png)
![kayıt ekranı](https://github.com/ertrldtcu/YazLab/blob/master/I/I/screenshots/register.png)
![liste ekranı](https://github.com/ertrldtcu/YazLab/blob/master/I/I/screenshots/list.png)
![harita ekranı](https://github.com/ertrldtcu/YazLab/blob/master/I/I/screenshots/map.png)
</details>

<hr>

<details>
<summary>Multithread Kullanarak Samurai Sudoku Çözme</summary>

Bu projede bizden 5 ve 10 thread kullanarak samurai sudoku çözen masaüstü uygulaması istenmiştir. Çözülmesi gereken samurai sudoku tipi belli olan dosya üzerinden okunmaktadır. Okunan samurai sudoku hem 5 hem de 10 thread ile ayrı ayrı çözülmektedir. Çözüm algoritması olarak backtracking kullanılmıştır. Çözüm sonucunda farklı thread sayılarına göre çözümün verim (bulunan kutu sayısı - zaman) grafiği çizdirilmektedir. Arayüz için **tkinter** kütüphanesini tercih ettik. Detaylı bilgi için [tıklayınız](https://github.com/ertrldtcu/YazLab/blob/master/I/II/proje2.pdf).

**Ekran Görüntüleri**
![çözülmemiş](https://github.com/ertrldtcu/YazLab/blob/master/I/II/screenshots/unsolved.png)
![5 thread ile çözüldükten sonra](https://github.com/ertrldtcu/YazLab/blob/master/I/II/screenshots/5%20thread.png)
![10 thread ile çözüldükten sonra](https://github.com/ertrldtcu/YazLab/blob/master/I/II/screenshots/10%20thread.png)
</details>

<hr>

<details>
<summary>Web Uygulaması (PDF İşleme)</summary>

Bu projede bizden, yapılan projelerin sisteme yüklenebildiği ve raporun temel bilgilerinin çıkarılıp sorgulanabildiği bir web uygulaması istenmiştir. Web sitesinde kullanıcı ve yöneticiler için farklı arayüzler bulunmaktadır. Kullanıcılar sisteme sadece PDF yükleyebilirken, yöneticiler hem kullanıcı ekleme, silme, düzenleme işlemlerini yapabilmekte hem de yüklenen tüm PDF'leri görüntüleyebilmektedir. Hem kullanıcılar hem de yöneticiler görüntüleyebildikleri PDF'ler için sorgu yapabilmektedir. Web sitesi iskeleti için **flask** kütüphanesini tercih ettik. PDF'lerden temel bilgileri alabilmek için **pdfminer** ve **regex** kütüphanelerinden yararlandık. Detaylı bilgi için [tıklayınız](https://github.com/ertrldtcu/YazLab/blob/master/I/III/proje3.pdf).

**Ekran Görüntüleri**
![kullanıcı girişi](https://github.com/ertrldtcu/YazLab/blob/master/I/III/screenshots/userlogin.png)
![yönetici girişi](https://github.com/ertrldtcu/YazLab/blob/master/I/III/screenshots/adminlogin.jpg)
![kullanıcı ekranı](https://github.com/ertrldtcu/YazLab/blob/master/I/III/screenshots/user%20screen.png)
![yönetici kullanıcılar ekranı](https://github.com/ertrldtcu/YazLab/blob/master/I/III/screenshots/admin%20users%20screen.png)
![yönetici dosyalar ekranı](https://github.com/ertrldtcu/YazLab/blob/master/I/III/screenshots/admin%20files%20screen.png)
</details>

<hr>