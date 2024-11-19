# TP1 : Premiers pas GNS, Cisco et VLAN

Premier TP, où on prend surtout les marques avec l'environnement GNS3, et on aborde une première notion : les VLANs.

![best memes from cisco doc](./img/the-best-memes-come-from-cisco-documentation.jpg)

# Sommaire

- [TP1 : Premiers pas GNS, Cisco et VLAN](#tp1--premiers-pas-gns-cisco-et-vlan)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. Dumb switch](#i-dumb-switch)
  - [1. Topologie 1](#1-topologie-1)
  - [2. Adressage topologie 1](#2-adressage-topologie-1)
  - [3. Setup topologie 1](#3-setup-topologie-1)
- [II. VLAN](#ii-vlan)
  - [1. Topologie 2](#1-topologie-2)
  - [2. Adressage topologie 2](#2-adressage-topologie-2)
    - [3. Setup topologie 2](#3-setup-topologie-2)
- [III. Ptite VM DHCP](#iii-ptite-vm-dhcp)

# 0. Prérequis

➜ **GNS3 installé et prêt à l'emploi**

- [GNS3VM](https://www.gns3.com/software/download-vm) fonctionnelle
- de quoi faire tourner un switch Cisco
  - [IOU2 L2 dispo ici (switch)](http://dl.nextadmin.net/dl/EVE-NG-image/iol/bin/i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin)
- de quoi faire tourner un routeur Cisco
  - [image d'un 7200 dispo ici (routeur)](https://lms.onnocenter.or.id/pustaka/docs/GNS3/images/c7200-a3jk9s-mz.124-25g.bin)

> *Le hash MD5 de cette image est 3a78cb61831b3ef1530f7402f5986556 si vous voulez vérifier.*

➜ **Les clients seront des VPCS**

- c'est un truc de GNS pour simuler un client du réseau
- quand on veut juste un truc capable de faire des pings et rien de plus, c'est parfait
- ça consomme R en ressources

# I. Dumb switch

## 1. Topologie 1

![Topologie 1](./img/topo1.png)

## 2. Adressage topologie 1

| Node  | IP            |
| ----- | ------------- |
| `pc1` | `10.3.1.1/24` |
| `pc2` | `10.3.1.2/24` |

## 3. Setup topologie 1

🌞 **Commençons simple**

- définissez les IPs statiques sur les deux VPCS
- `ping` un VPCS depuis l'autre
- afficher la CAM table (voir juste en dessous) du switch et vérifier les MAC qui s'y trouvent

La *CAM table* c'est un tableau qu'entretient un switch et qui liste toutes les adresses MAC qu'il connaît.

Dès que quelqu'un envoie une trame qui traverse le switch, **il apprend la MAC de la machine branchée sur ce port.** Il l'enregistre alors dans sa *CAM table*.

Ainsi, la *CAM table* contient les adresses MAC de toutes les machines qui ont déjà envoyé une trame sur le réseau, quand on a un seul switch où tout est branché, comme ici.

> Jusque là, ça devrait aller. Noter qu'on a fait aucune conf sur le switch. Tant qu'on ne fait rien, c'est une bête multiprise.

# II. VLAN

**Le but dans cette partie va être de tester un peu les *VLANs*.**

On va rajouter **un troisième client** qui, bien que dans le même réseau, sera **isolé des autres grâce aux *VLANs***.

**Les *VLANs* sont une configuration à effectuer sur les *switches*.** C'est les *switches* qui effectuent le blocage.

Le principe est simple :

- déclaration du VLAN sur tous les switches
  - un VLAN a forcément un ID (un entier)
  - bonne pratique, on lui met un nom
- sur chaque switch, on définit le VLAN associé à chaque port
  - genre "sur le port 35, c'est un client du VLAN 20 qui est branché"

![VLAN FOR EVERYONE](./img/get_a_vlan.jpg)

## 1. Topologie 2

![Topologie 2](./img/topo2.png)

## 2. Adressage topologie 2

| Node  | IP            | VLAN |
| ----- | ------------- | ---- |
| `pc1` | `10.3.1.1/24` | 10   |
| `pc2` | `10.3.1.2/24` | 10   |
| `pc3` | `10.3.1.3/24` | 20   |

### 3. Setup topologie 2

🌞 **Adressage**

- définissez les IPs statiques sur tous les VPCS
- vérifiez avec des `ping` que tout le monde se ping

🌞 **Configuration des VLANs**

- référez-vous [à la section VLAN du mémo Cisco](../../cours/memo/memo_cisco.md#8-vlan)
- déclaration des VLANs sur le switch `sw1`
- ajout des ports du switches dans le bon VLAN (voir [le tableau d'adressage de la topo 2 juste au dessus](#2-adressage-topologie-2))
  - ici, tous les ports sont en mode *access* : ils pointent vers des clients du réseau

🌞 **Vérif**

- `pc1` et `pc2` doivent toujours pouvoir se ping
- `pc3` ne ping plus personne

![i know cisco](./img/i_know.jpeg)

# III. Ptite VM DHCP

On va ajouter une VM dans la topologie, histoire que vous voyiez cet aspect de GNS.

| Node          | IP              | VLAN |
| ------------- | --------------- | ---- |
| `pc1`         | `10.3.1.1/24`   | 10   |
| `pc2`         | `10.3.1.2/24`   | 10   |
| `pc3`         | `10.3.1.3/24`   | 20   |
| `pc4`         | X               | 20   |
| `pc5`         | X               | 10   |
| `dhcp.tp3.b2` | `10.3.1.253/24` | 20   |

🌞 **VM `dhcp.tp3.b2`**

- Rocky Linux 9, IP statique, nom défini à `dhcp.tp3.b2`, SELinux désactivé, firewall activé, système à jour
- installez un serveur DHCP
  - il doit délivrer des IPs entre `10.3.1.100` et `10.3.1.200`
  - je vous recommande de suivre [ce lien](https://www.server-world.info/en/note?os=Rocky_Linux_8&p=dhcp&f=1) pour setup le serveur DHCP (je sais que c'est pour Rocky8, mais ça n'a pas bougé l'install/conf de ce serveur DHCP)
  - **vous n'avez le droit d'utiliser QUE des lignes que vous comprenez dans le fichier de conf, et qui ont une utilité ici**
- vérifier avec le `pc4` que vous pouvez récupérer une IP en DHCP
- vérifier avec le `pc5` que vous ne pouvez PAS récupérer une IP en DHCP

> Pour rappel, la trame DHCP Discover part en broadcast. Le switch bloque ça aussi, il bloque tout, il s'en fout de la nature de la trame : si ça passe d'un port taggé VLAN X à un port taggé VLAN Y, ça dégage.
