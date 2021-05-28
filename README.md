# RL-QLearning
Q Learning, bir Reinforcement Learning (Pekiştirmeli Öğrenme) algoritmasıdır.

Robota engelleri öğretmeyi ve öğrenme tamamlandıktan sonra hedefe engellere çarpmadan ulaşmasını hedefler.

Q Learning algoritması, ödül - ceza prensibini benimsemiştir.

Kullanıcının gireceği değerlere bağlı başlangıç-hedef noktaları belirlendikten sonra alanın %30'unu kapsayan engeller random olarak atanacaktır. Bu nedenle proje her çalıştırıldığında engellerin konumu farklı olarak gelecek ve öğrenme yeniden başlayacaktır.

Projede robota engele çarpma cezası olarak -30 puan, her adımın cezası -0.3 puan ve hedefe ulaşmanın ödülü +100 puan olarak belirlenmiştir.

Robot her engele çarptığında ya da hedefe ulaştığında başlangıç noktasına geri dönecektir.

Q Matrisi her hamlesinde sürekli güncellenecek ve en optimal yol bir süre tekrarlanmaya başlaycaktır.

En optimal yol bulunduğunda ise bu yol arayüzde gösterilecek, episode via steps - episode via cost grafikleri çizdirilecektir.



(NOT: Ajan aşağı, yukarı, sağ, sol ve çarpraz hareket edebilmekte ve her yönde aynı cezayı almaktadır. Çarpraz adımın diğer adımlardan bir farkı olmadığından zaman zaman çarpraz hamleyi daha optimal bulacak ve o yöne hareket edecektir.)
