# Procédures

Vous trouverez ici quelques mini-procédures pour réaliser certaines opérations récurrentes. Ce sera évidemment principalement utilisé pour notre cours de réseau, mais peut-être serez-vous amenés à le réutiliser plus tard.

**Elles sont écrites pour un système Cisco**.

# Sommaire

<!-- vim-markdown-toc GitLab -->

- [Procédures](#procédures)
- [Sommaire](#sommaire)
- [I. Les modes du terminal](#i-les-modes-du-terminal)
- [II. Commandes](#ii-commandes)
  - [1. Définir une IP statique](#1-définir-une-ip-statique)
  - [2. Définir une IP dynamiquement](#2-définir-une-ip-dynamiquement)
  - [3. Garder les changements après reboot](#3-garder-les-changements-après-reboot)
  - [4. Ajouter une route statique](#4-ajouter-une-route-statique)
  - [5. Changer son nom de domaine](#5-changer-son-nom-de-domaine)
  - [6. Gérer sa table ARP](#6-gérer-sa-table-arp)
  - [7. Configuration d'un NAT simple](#7-configuration-dun-nat-simple)
  - [8. VLAN](#8-vlan)
    - [Mode *access*](#mode-access)
    - [Mode trunk](#mode-trunk)
  - [9. STP](#9-stp)
  - [10. OSPF](#10-ospf)
  - [11. LACP](#11-lacp)
  - [12. HSRP](#12-hsrp)

<!-- vim-markdown-toc -->

---

# I. Les modes du terminal

Le terminal Cisco possède plusieurs modes

Mode | Commande | What ? | Why ?
--- | --- | --- | ---
`user EXEC` | X | C'est le mode par défaut : il permet essentiellement de visualiser des choses, mais peu d'actions à réaliser | Pour visualiser les routes ou les IPs par ex
`privileged EXEC` | enable | Mode privilégié : permet de réalisé des actions privilégiées sur la machine | Peu utilisé dans notre cours au début
`global conf` | conf t | Configuration de la machine | Permet de configurer les interface et le routage

L'idée globale c'est que pour **faire des choses** on passera en `global conf` pour **faire** des choses, et on restera en **user EXEC** pour **voir** des choses.

# II. Commandes

## 1. Définir une IP statique

➜ **1. Repérer le nom de l'interface dont on veut changer l'IP**

```cisco
# show ip interface brief
OU
# show ip int br
```

➜ **2. Passer en mode configuration d'interface**

```cisco
# conf t
(config)# interface ethernet <NUMERO>
```

➜ **3. Définir une IP**

```cisco
(config-if)# ip address <IP> <MASK>
Exemple :
(config-if)# ip address 10.5.1.254 255.255.255.0
```

➜ **4. Allumer l'interface**

```cisco
(config-if)# no shut
```

➜ **5. Vérifier l'IP**

```cisco
(config-if)# exit
(config)# exit
# show ip int br
```

## 2. Définir une IP dynamiquement

Une IP définie dynamiquement est une IP récupérée *via* DHCP.

➜ **1. Repérer le nom de l'interface dont on veut changer l'IP**

```cisco
# show ip interface brief
OU
# show ip int br
```

➜ **2. Passer en mode configuration d'interface**

```cisco
# conf t
(config)# interface ethernet <NUMERO>
```

➜ **3. Définir une IP**

```cisco
(config-if)# ip address dhcp
```

➜ **4. Allumer l'interface**

```cisco
(config-if)# no shut
```

➜ **5. Vérifier l'IP**

```cisco
(config-if)# exit
(config)# exit
# show ip int br
```

## 3. Garder les changements après reboot

Les équipements Cisco possèdent deux configurations (d'une certain façon) :

- la `running-config`
  - c'est la conf actuelle
  - elle contient toutes vos modifications
  - `# show running-config` pour la voir
- la `startup-config`
  - c'est la conf qui est chargée au démarrage de la machine
  - elle ne contient aucune de vos modifications
  - `show startup-config`

Comment garder vos changements à travers les reboots ? Il faut copier la `running-config` sur la `startup-config` :

```cisco
# copy running-config startup-config
```

## 4. Ajouter une route statique

➜ **1. Passer en mode configuration**

```cisco
# conf t
```

➜ **2.1. Ajouter une route vers un réseau**

```cisco
(config)# ip route <REMOTE_NETWORK_ADDRESS> <MASK> <GATEWAY_IP>

Exemple : ajouter une route vers le réseau 10.1.0.0/24 en passant par la passerelle 10.2.0.254
(config)# ip route 10.1.0.0 255.255.255.0 10.2.0.254
```

➜ **2.2. Ajouter la route par défaut**

```cisco
(config)# ip route 0.0.0.0 0.0.0.0 10.2.0.254
```

➜ **3. Vérifier la route**

```cisco
(config)# exit
# show ip route
```

## 5. Changer son nom de domaine

➜ **1. Passer en mode configuration**

```cisco
# conf t
```

➜ **2. Changer le hostname**

```cisco
(config)# hostname <HOSTNAME>
```

## 6. Gérer sa table ARP

- voir sa table ARP

```cisco
# show arp
```

## 7. Configuration d'un NAT simple

Configuration des interfaces "externes" et "internes" :

- "externes" : les interfaces qui pointent vers le WAN
- "internes" : les interfaces qui pointent vers des LANs

➜ **1. Repérage des interfaces "internes" et "externes"**

```cisco
# show ip int br
```

➜ **2. Passer en mode config**

```cisco
# conf t
```

➜ **3. Configurer les interfaces en "interne" ou "externe"**

```cisco
Interfaces "externes" :
(config)# interface fastEthernet 0/0
(config-if)# ip nat outside
(config-if)# exit

Interfaces "internes" :
(config)# interface fastEthernet 1/0
(config-if)# ip nat inside
(config-if)# exit

(config)# interface fastEthernet 2/0
(config-if)# ip nat inside
(config-if)# exit
```

➜ **4. Définir une liste où tout le trafic est autorisé**

```cisco
(config)# access-list 1 permit any
```

➜ **5. Configurer le NAT**

```cisco
(config)# ip nat inside source list 1 interface <OUTSIDE_INTERFACE> overload
Par exemple :
(config)# ip nat inside source list 1 interface fastEthernet 0/0 overload
```

## 8. VLAN

### Mode *access*

**Que sur des switches.**

**N'utilisez pas le VLAN 1.**

Le mode *access* permet de définir un port d'un switch dans un VLAN donné. On dit du client qui est branché à ce port qu'il est "dans" ce VLAN.

➜ **1. Passer en mode configuration**

```cisco
# conf t
```

➜ **2. Définir les VLANs à utiliser**

```cisco
(config)# vlan 10
(config-vlan)# name admins
(config-vlan)# exit

(config)# vlan 20
(config-vlan)# name guests
(config-vlan)# exit

(config)# exit
# show vlan
```

➜ **3. Attribuer à chaque interface du switch un VLAN**

```cisco
# conf t
(config)# interface fastEthernet0/0
(config-if)# switchport mode access
(config-if)# switchport access vlan 10
(config-if)# exit
```

➜ **4. Vérifier les changements**

```cisco
# show vlan br
```


### Mode trunk

Le mode *trunk* permet de définir quels VLANs seront autorisés à circuler entre deux équipements réseau, typiquement deux switches.

➜ **1. Passer en mode configuration**

```cisco
# conf t
```

➜ **2. Définir les VLANs à utiliser**

```cisco
(config)# vlan 10
(config-vlan)# name admins
(config-vlan)# exit

(config)# vlan 20
(config-vlan)# name guests
# show vlan
```

➜ **3. Attribuer un trunk entre deux équipements**

```cisco
# conf t
(config)# interface fastEthernet0/0
(config-if)# switchport trunk encapsulation dot1q
(config-if)# switchport mode trunk
(config-if)# switchport trunk allowed vlan add 10,20
(config-if)# exit
(config)# exit
# show interface trunk
```

## 9. STP

➜ Voir la conf actuelle

```cisco
# show spanning-tree
```

➜ Modifier la priorité d'une interface

```cisco
sw1(config)#interface Ethernet0/0
sw1(config-if)#spanning-tree vlan 1 port-priority 50
```

## 10. OSPF

➜ Configurer OSPF

```cisco
# Activation de OSPF
R3(config)#router ospf 1

# Définition arbitraire d'un router-id
R3(config-router)#router-id 3.3.3.3

# Partage du réseau 10.1.1.0/24
# Notez bien la notation du masque en inversé
R3(config-router)#network 10.1.1.0 0.0.0.255 area 0

# si R3 a accès internet, il peut partager sa route par défaut dans OSPF
R3(config-router)#default-information originate always 
```

➜ Voir la conf

```cisco
R3# show ip route
R3# show ip ospf
R3# show ip ospf neighbor
R3# show ip ospf ?     # pour + de commandes et de détails
```

## 11. LACP

> On suppose deux switches qui sont reliés par deux câbles. Le but est donc d'agréger, sur chaque switch, les deux ports. Pour simuler un seul "gros" port redondé par deux liens.

➜ **Configurez les VLANs au préalable sur les deux switches**

- ou en même temps, mais d'abord déclaration de VLAN
- et ensuite déclaration de l'agrégation de ports

```cisco
interface FastEthernet0/1  # on ajoute une première interface au port-channel
 switchport ... # config VLAN
 channel-group 1 mode on  # 1 c'est l'ID du port-channel
 exit
interface FastEthernet0/2  # puis la deuxième
 switchport ... # config VLAN
 channel-group 1 mode on
```

Voir l'état de LACP (Etherchannel) :

```cisco
show etherchannel ?
show etherchannel summary
show etherchannel load-balance
etc.
```

## 12. HSRP

> *On suppose R1 10.1.1.1, R2 10.1.1.2 et l'IP virtuelle voulue 10.1.1.3.*

Sur R1, celui qui sera prioritaire :

```cisco
interface fe 1/0
 ip address 10.1.1.1 255.255.255.0
 no shutdown
 standby 10 ip 10.1.1.3
 standby 10 priority 150
 standby 10 preempt
```

Sur R2 :

```cisco
interface fe 1/0
 ip address 10.1.1.2 255.255.255.0
 no shutdown
 standby 10 ip 10.1.1.3
 standby 10 priority 100
```

Voir l'état de HSRP :

```
R2# show standby
R2# show standby brief
```
