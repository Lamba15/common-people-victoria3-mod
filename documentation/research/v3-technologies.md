# V3 Technologies Affecting Common People

## Technology Categories

V3 has 3 tech trees with ~178 total technologies across 5 eras (1836-1936+). Countries start with 20-30 techs; leading nations research ~1/year.

## Technologies That Matter for Our Mod

### Agriculture
- **Enclosure** (Era 1) -- Unlocks agriculture buildings
- **Cotton Gin** (Era 1) -- +25% cotton plantation throughput
- **Sericulture** (Era 1) -- +25% silk plantation throughput

### Factories
- **Manufactories** (Era 1) -- Unlocks Food Industries, Textile Mills, Glassworks, Paper Mills, Furniture, Tooling
- **Steelworking** (Era 1) -- Steel Mills
- **Atmospheric Engine** (Era 2) -- Motor Industries
- **Bessemer Process** (Era 2) -- Better steel production
- **Electrical Generation** (Era 3) -- Power Plants
- **Combustion Engine** (Era 3+) -- Automobiles, Oil Derricks

### Railways
- **Railways** (Era 2) -- Railway building, public trams

### Health/Medicine
- **Medical Degrees** -- Public health when administrators trained
- **Quinine** -- Disables malaria
- **Malaria Prevention** -- Disables severe malaria
- **Antibiotics** -- Reduces disease outbreak impact
- **Pharmaceuticals** -- Enables health insurance institutions

### Education
- **Rationalism** -- +0.5 education access per SoL
- **Empiricism** -- +0.5 education access per SoL
- **Dialectics** -- +0.5 education access per SoL
- **Academia** -- Unlocks university buildings

### Labor and Society
- **Labor Movement** -- Unlocks workplace safety regulations
- **Feminism** -- Unlocks feminist ideology, enables women's suffrage
- **Egalitarianism** -- Supports universal suffrage
- **Human Rights** -- Worker protections and education laws
- **Anarchism** -- Alternative economic ideology
- **Socialism** -- Enables command economy and cooperative ownership
- **Central Planning** -- Unlocks command economy system

### Military (Conscription-Relevant)
- **Standing Army** -> Hussars
- **Line Infantry** -> Line Infantry, Dragoons
- **Artillery** -> Cannon Artillery
- **General Staff** -> Skirmish Infantry
- **Handcranked Machine Gun** -> +5 Army defense
- **Dreadnought, Battleship, Aircraft Carrier** -> Capital ships

## How Technology Affects Pops

### Standard of Living
- Education techs provide +0.5 education access per SoL each
- Higher SoL = more/better goods consumed = higher expenses
- Literacy is the hard cap on innovation use

### Wages
- Advanced production methods = higher output BUT require educated workers
- Mechanization reduces worker count but increases skill requirements
- Creates demand for qualified labor while displacing unskilled workers

### Working Conditions
- Labor Movement unlocks Workplace Safety (reduces mortality)
- Health techs reduce disease mortality
- Children's Rights and Women's Rights change workforce composition

## Detecting Technology in Script

```
# Check if a country has researched a technology
has_technology_researched = technology_name

# Example: check if railways have been researched
has_technology_researched = railways
```

Technology files location: `/Victoria 3/game/common/technology/technologies/`
