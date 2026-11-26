# Datos de la sesión 3

Dos tablas del análisis del curso sobre AlphaFold. Son el resultado ya calculado: no hay que
volver a ejecutar nada, y no se modifican. Las copias originales están en
`caso-alphafold/analisis/resultados/` del repositorio del curso.

**La pregunta:** ¿la confianza de AlphaFold en el bolsillo avisa de si el docking va a funcionar?

## De dónde salen

- **PoseBusters Benchmark set** (Buttenschoen et al., *Chemical Science* 2024): 428 complejos
  proteína-ligando del PDB, todos publicados desde 2021, filtrados por calidad.
- **Modelos de AlphaFold DB**, versión 6, descargados el 25/11/2026.
- La correspondencia entre cadena del PDB y proteína de UniProt viene de SIFTS (PDBe).

## Palabras que hacen falta

| Palabra | Qué es |
|---|---|
| Complejo | Una estructura medida en el laboratorio en la que se ve la proteína y el ligando pegado en su sitio |
| Ligando | La molécula pequeña que se une a la proteína: un fármaco o un candidato |
| Bolsillo | El hueco de la proteína donde se mete el ligando. Aquí: los aminoácidos con algún átomo a menos de 6 Å del ligando |
| pLDDT | La confianza que AlphaFold se da a sí mismo en cada aminoácido, de 0 a 100 |
| RMSD | Distancia media entre los mismos átomos en dos estructuras, en ångströms (Å). Cuanto menor, más se parecen |
| Docking | Un programa que intenta colocar el ligando dentro del bolsillo. Por convenio, acierta si la postura queda a menos de 2 Å de la real |

## bolsillos.csv · una fila por complejo

428 filas, una por complejo de PoseBusters. **No todas sirven:** la columna `estado` dice qué
pasó con cada una. Hay 384 con `estado` igual a `ok`; de ellas, el análisis del curso se quedó
con las 374 que además tienen `identidad_bolsillo` de 0,9 o más.

| Columna | Qué es |
|---|---|
| complejo | Código del complejo: estructura del PDB y ligando (`5SAK_ZRY`) |
| pdb | Código de la estructura experimental |
| ligando | Código del ligando |
| cadena | Cadena de la estructura que se ha usado |
| n_bolsillo | Cuántos aminoácidos forman el bolsillo |
| uniprot | Identificador de la proteína. **Una misma proteína aparece en varias filas** |
| af_version | Versión del modelo de AlphaFold DB |
| n_mapeados | Aminoácidos del bolsillo encontrados también en el modelo |
| identidad_bolsillo | Qué parte del bolsillo coincide en secuencia entre estructura y modelo (de 0 a 1) |
| plddt_bolsillo | Confianza media de AlphaFold en el bolsillo |
| plddt_min_bolsillo | La confianza del peor aminoácido del bolsillo |
| plddt_global | Confianza media de toda la proteína |
| rmsd_ca_bolsillo | Diferencia con el bolsillo experimental usando solo el esqueleto (carbonos α) |
| rmsd_atomos_bolsillo | Diferencia usando todos los átomos pesados comunes |
| n_atomos | Cuántos átomos se han comparado |
| long_uniprot | Longitud de la proteína entera |
| estado | `ok`, o el motivo por el que ese complejo se quedó fuera |

## docking_caja_ajustada.csv · una fila por complejo acoplado

90 complejos, uno por proteína, repartidos en cuatro tramos de confianza. Cada ligando se
acopló **dos veces** con AutoDock Vina: sobre el modelo de AlphaFold y sobre la estructura
experimental. La segunda es el control: dice qué casos sabe resolver el programa.

| Columna | Qué es |
|---|---|
| complejo, uniprot | Como en la otra tabla |
| caja_A | Lado de la caja de búsqueda, en ångströms |
| metal_en_bolsillo | Si hay un ion metálico en el bolsillo |
| energia_af, rmsd_af, rmsd_min_af, acierta_af, n_poses_af | Resultado sobre el modelo de AlphaFold |
| energia_exp, rmsd_exp, … , acierta_exp | Lo mismo sobre la estructura experimental (el control) |
| acierta_… | Verdadero si la mejor postura queda a menos de 2 Å de la real |
| plddt_bolsillo, rmsd_atomos_bolsillo | Copiadas de la otra tabla, para no tener que cruzarlas |

## Lo que estas cifras no pueden decir

- Las cifras absolutas de acierto **no son comparables con la literatura**: la preparación del
  receptor fue básica (receptor rígido, protonación sin revisar, modelo sin minimizar), y
  PoseBusters es un conjunto difícil a propósito.
- La caja de búsqueda se centró en el ligando experimental: en un caso real no se sabe dónde
  está el sitio de unión.
- Una sola cadena por complejo, sin cofactores ni otras cadenas.
- Los modelos de AlphaFold DB son de 2025 y pudieron usar como plantilla estructuras del PDB
  posteriores a 2021: si acaso, los bolsillos se parecerían más de lo debido.

El método completo y los límites están en `caso-alphafold/analisis/LEEME.md` del repositorio
del curso. Cita a Buttenschoen et al. (2024) si usas estos datos.
