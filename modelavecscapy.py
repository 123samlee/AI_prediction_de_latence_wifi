from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Elt
import joblib


svm_model = joblib.load('new_svm_model.pkl')
packets = sniff(offline="infoswifi.pcap")

# Dictionnaire pour stocker les informations sur les réseaux WiFi et leur latence prédite
wifi_networks = {}

# Fonction de traitement des paquets capturés
def process_packet(packet, distance):
    if packet.haslayer(Dot11) and packet.type == 0 and packet.subtype == 8:  # Vérifie si le paquet est une trame de gestion Beacon
        ssid = packet[Dot11Elt].info.decode()  # Extrait le SSID du réseau WiFi
        bssid = packet.addr3  # Adresse BSSID du point d'accès
        rssi = packet.dBm_AntSignal  # Extrait la valeur RSSI du paquet

        # Calcul de la latence prédite en utilisant le modèle SVM
        latence_predite = svm_model.predict([[rssi, distance]])

        # Ajouter les informations sur le réseau WiFi et la latence prédite au dictionnaire
        wifi_networks[ssid] = {'bssid': bssid, 'rssi': rssi, 'latence': latence_predite[0]}

# Distance manuelle
distance_manuelle = 0 # Mettez la distance désirée ici en mètres




# Traiter les paquets capturés
for packet in packets:
    process_packet(packet, distance_manuelle)

# Afficher toutes les latences prédites pour chaque réseau WiFi
print("Latences prédites pour chaque réseau WiFi :")
for ssid, info in wifi_networks.items():
    print(f"SSID: {ssid}, BSSID: {info['bssid']}, RSSI: {info['rssi']} dBm, Latence prédite: {info['latence']} ms")

# Trouver le réseau WiFi avec la latence prédite la plus faible
meilleur_reseau = min(wifi_networks, key=lambda x: wifi_networks[x]['latence'])
print(f"\nLe meilleur réseau WiFi est '{meilleur_reseau}' avec une latence prédite de {wifi_networks[meilleur_reseau]['latence']} ms.")
