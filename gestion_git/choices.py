# CODIGOS DE IMPUESTO GIT
impuestos = (
    ('2', 'ISIB CM'),
    ('4', 'ISIB RG'),
    ('3', 'AP'),
    ('5','PF Caduco'),
    ('7','ABL'),
    ('8', 'RV'),
    ('10', 'Abasto'),
    ('11', 'Mesas y Sillas'),
    ('12', 'Volquetes'),
    ('13', 'Kioscos'),
    ('14', 'Vallas'),
    ('16', 'Toldos'),
    ('17', 'Postes'),
    ('19', 'Uso del Subsuelo'),
    ('20', 'ISIB AR'),
    ('21', 'SIRCREB'),
    ('27', 'Embarcaciones'),
    ('28', 'Sellos'),
    ('30', 'Moratoria RV-ABL'),
    ('31', 'Antenas'),
    ('40', 'ISIB RS'),
    ('100','Multa DGDyPC')
    
)

# JUZGADOS Y SECRETARIAS CAYT
juzgados = (
    ('1','1'),('2','2'),
    ('3','3'),('4','4'),
    ('5','5'),('6','6'),
    ('7','7'),('8','8'),
    ('9','9'),('10','10'),
    ('11','11'),('12','12'),
    ('13','13'),('14','14'),
    ('15','15'),('16','16'),
    ('17','17'),('18','18'),
    ('19','19'),('20','20'),
    ('21','21'),('22','22'),
    ('23','23'),('24','24'),
)

secretarias = (
    ('1','1'),('2','2'),('3','3'),('4','4'),
    ('5','5'),('6','6'),('7','7'),('8','8'),
    ('9','9'),('10','10'),('11','11'),('12','12'),
    ('13','13'),('14','14'),('15','15'),('16','16'),
    ('17','17'),('18','18'),('19','19'),('20','20'),
    ('21','21'),('22','22'),('23','23'),('24','24'),
    ('25','25'),('26','26'),('27','27'),('28','28'),
    ('29','29'),('30','30'),('31','31'),('32','32'),
    ('33','33'),('34','34'),('35','35'),('36','36'),
    ('37','37'),('38','38'),('39','39'),('40','40'),
    ('41','41'),('42','42'),('43','43'),('44','44'),
    ('45','45'),('46','46'),('47','47'),('48','48'),
)

# MANDATARIOS CREADOS
seccion = (
    ('Adriano Sarubbi','2'),
    ('Carla Sarubbi','83'),
    ('Maria Masanti','111'),
    ('Francisco Pérez Chada','147'),
)

# CHOICES EN EMBARGOS

tipo_de_embargo = (
('Preventivo','Preventivo'),
('Ejecutorio','Ejecutorio')
)


clase_embargo = (
    ('SOJ', 'SOJ'),
    ('BCRA', 'BCRA')
)

estado_embargo = (
    ('Trabado', 'Trabado'),
    ('Lev.solicitado','lev.solicitado'),
    ('Levantado', 'Levantado'),
    ('Embargo', 'Embargo'),
    ('S/Oficio', 'S/Oficio'),
    

)

orden_de_levantamiento = (
    ('si', 'Si'),
    ('no', 'No')
)

# CHOICES EN PLANES DE PAGO

mod_pago = (
    ('Contado','Contado'),
    ('Cuotas', 'Cuotas')
)

cuotas = (
    ('1','1'),('2','2'),('3','3'),('4','4'),
    ('5','6'),('6','6'),('7','7'),('8','8'),
    ('9','9'),('10','10'),('11','11'),('12','12'),
    ('13','13'),('14','14'),('15','15'),('16','16'),
    ('17','17'),('18','18'),('19','19'),('20','20'),
    ('21','21'),('22','22'),('23','23'),('24','24'),
    ('25','25'),('26','26'),('27','27'),('28','28'),
    ('29','29'),('30','30'),('31','31'),('32','32'),
    ('33','33'),('34','34'),('35','35'),('36','36'),
)

cuotas_hono = (
    ('1','1'),('2','2'),('3','3'),('4','4'),
    ('5','5'),('6','6')
)

comprobante = (
    ('si', 'Si'),
    ('no', 'No'),
)

estado_plan = (
     ('Pendiente', 'Pendiente'),
     ('Nulo', 'Nulo'),
     ('Cancelado', 'Cancelado'),
     ('Vigente', 'Vigente')
)

bancos = (
    ('Banco B.I. Creditanstalt Sociedad Anonim','147'),
    ('Banco Cmf S.A.','319'),
    ('Banco Columbia S.A.','389'),
    ('Banco Comafi Sociedad Anonima','299'),
    ('Banco Credicoop Cooperativo Limitado','191'),
    ('Banco De Corrientes S.A.','94'),
    ('Banco De Formosa S.A.','315'),
    ('Banco De Galicia Y Buenos Aires S.A.','7'),
    ('Banco De La Ciudad De Buenos Aires','29'),
    ('Banco De La Nacion Argentina','11'),
    ('Banco De La Pampa Sociedad De Economía M','93'),
    ('Banco De La Provincia De Buenos Aires','14'),
    ('Banco De La Provincia De Cordoba S.A.','20'),
    ('Banco De San Juan S.A.','45'),
    ('Banco De Santa Cruz S.A.','86'),
    ('Banco De Santiago Del Estero S.A.','321'),
    ('Banco De Servicios Y Transacciones S.A.','338'),
    ('Banco De Valores S.A.','198'),
    ('Banco Del Chubut S.A.','83'),
    ('Banco Del Sol S.A.','310'),
    ('Banco Finansur S.A.','303'),
    ('Banco Hipotecario S.A.','44'),
    ('Banco Itau Buen Ayre S.A.','259'),
    ('Banco Julio Sociedad Anonima','305'),
    ('Banco Macro S.A.','285'),
    ('Banco Mariva S.A.','254'),
    ('Banco Masventas Sa','341'),
    ('Banco Meridian S.A.','281'),
    ('Banco Municipal De Rosario','65'),
    ('Banco Patagonia S.A.','34'),
    ('Banco Piano S.A.','301'),
    ('Banco Provincia De Tierra Del Fuego','268'),
    ('Banco Provincia Del Neuquén Sociedad Anó','97'),
    ('Banco Roela S.A.','247'),
    ('Banco Saenz S.A.','277'),
    ('Banco Santander Rio S.A.','72'),
    ('Banco Supervielle S.A.','27'),
    ('Bbva Banco Frances S.A.','17'),
    ('Bnp Paribas','266'),
    ('Citibank N.A.','16'),
    ('Hsbc Bank Argentina S.A.','150'),
    ('Jpmorgan Chase Bank, National Associatio','165'),
    ('Mba Banco De Inversiones S. A.','312'),
    ('Nuevo Banco De Entre Ríos S.A.','386'),
    ('Nuevo Banco De Santa Fe Sociedad Anonima','330'),
    ('Nuevo Banco Del Chaco S. A.','311'),
    ('Nuevo Banco Industrial De Azul S.A.','322'),
    ('Standard Bank Argentina S.A.','15'),
)