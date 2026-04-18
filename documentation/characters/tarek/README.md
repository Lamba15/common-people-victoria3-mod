# Tarek al-Rashidi (Egypt)

## Profile

- **Pop type**: Capitalist (spawns mid-game)
- **Culture**: Misri | **Religion**: Sunni | **Age**: 26 | **Traits**: Ambitious, Innovative
- **Full name**: Tarek al-Rashidi. Son of a landowner family from the Fayoum, not the Delta. A different region, a different family, but the same class as al-Sayyid. His father's estate failed when cotton prices collapsed. Tarek was nineteen. He mourned. Then he adapted.
- **Interest group**: Industrialists -- but he STARTED as Landowners. He crossed over.
- **Home state**: Cairo (factory) with a ghost in the Fayoum
- **Personality**: Ambitious, melancholic, forward-looking. He mourns the old world -- he loved his father's estate, the trees his grandfather planted, the view of the Fayoum at sunrise. But he chose to survive. There is grief underneath the European suit. He can't sleep and sometimes, late at night, he walks to the roof and stares south toward the Fayoum, missing the sound of the land.

## Personality Weights

| Interest | Weight | Why |
|----------|--------|-----|
| Industrialization | 10 | He bet everything on it |
| Economy | 10 | Profit is survival now |
| Land reform | 6 | Supports commercialized agriculture -- land as capital |
| Free trade | 9 | Exports are his lifeblood |
| Education | 7 | Literate workers operate better machines |
| Labor laws | 8 | OPPOSES them -- margins are thin, he can't afford kindness |
| France/diplomacy | 7 | French machines, French capital, French connections |
| War | 5 | Disrupts trade, but military contracts pay well |
| Landowners IG clout | 5 | Watches it fall with mixed feelings -- that was his world once |
| Religion | 4 | Respectful but distracted. God didn't save the estate. |

## What Makes Him Interesting

Tarek is NOT coldly pragmatic. He feels the loss of the old world. He remembers his father's estate and sometimes dreams about it. But he decided that grieving and dying is worse than grieving and building. He is the landowner class adapting instead of dying -- proof that abolishing serfdom doesn't abolish power, it forces power to change shape. He runs his factories the way his father's class ran estates: the workers are below, he is above. He tells himself it's different because they're free to leave. It is not very different.

**He doesn't drink** -- taboo for his culture/religion in V3. His grief shows up as sleeplessness on the roof, palms pressed into eyes, missing fajr prayer.

## Key V3 Hooks

```
# Spawn condition
AND = {
    country_has_primary_culture = cu:misri
    any_scope_building = { is_building_group = bg_manufacturing }
    NOR = {
        has_law = law_type:law_serfdom
        has_law = law_type:law_tenant_farmers
    }
}

# Industrialists IG gaining power
ig:ig_industrialists = {
    ig_clout >= 0.15
    is_in_government = yes
}

# Country industrializing (Tarek is thriving)
any_scope_building = {
    is_building_group = bg_manufacturing
}

# Economic freedom favors him
OR = {
    has_law = law_type:law_laissez_faire
    has_law = law_type:law_interventionism
}

# Cheap labor
has_law = law_type:law_no_workers_rights
```

On-actions: yearly pulse (economy test), `on_law_enacted` (labor laws), IG clout checks, building throughput in his state.

## Life Events

*Tarek appears when:* Country has factories AND land reform has moved past serfdom. He spawns mid-game -- he's a product of the transition, not the starting state.

*Tarek sells his father's land:*
His father died in debt. The Fayoum estate couldn't compete with modern agriculture. Tarek stood in the empty house, ran his hand along the wall his grandfather built, and then he locked the door and took a train to Cairo. He sold the land to a cotton company. He used the money to buy a share in a textile mill. On the train back he cried, quietly, looking out the window at fields that used to mean everything. Then he wiped his face and opened a ledger.

*Tarek's factory opens:*
He stands in his own factory for the first time. The machines are loud. The workers file in. He watches them and for a moment sees his father's fellahin walking to the fields at dawn. The similarity makes him uncomfortable. He pushes the thought away. "This is different. They're free. They chose to be here." They chose between this and starvation, but Tarek doesn't think about that part.

*Workers demand rights:*
"I understand them. I do. But the margins are thin. If I raise wages, I close. If I close, they have nothing. I'm not their enemy -- the market is." He almost believes this.

*Labor laws enacted:*
"Do you know what this costs? Do you know how many I'll have to let go? They think regulation protects the poor -- it creates the poor." He sits in his office running numbers. The numbers don't work. He presses his palms into his eyes and stays there a long time.

*Late at night, alone:*
Tarek sits on the roof of his Cairo apartment after midnight. Nice building. A view of the Nile. He holds a small framed photograph of the Fayoum estate -- the only thing he kept. He can hear the factory district humming even at this hour. He misses the quiet. He misses the smell of the earth after rain. He misses the call to fajr prayer echoing across flat fields. He does not miss being poor. He does not know if he is happy. He is rich. That will have to be enough.

*Tarek dies:*
His factories are sold to a European trading company. His daughter married a French merchant and lives in Marseille. Nobody in the Fayoum remembers the al-Rashidi name. The estate is a cotton processing plant now. The trees his grandfather planted were cut down for the rail line.

## Story Tree

```
TAREK SPAWNS (mid-game, factories exist, land reform past serfdom)
  Pop type: Capitalist | Home state: Cairo | IG: Industrialists
  |
  v
[TAREK OPENS HIS FACTORY]
  Mirror event: the player sees him cut the ribbon.
  His workers file in. He remembers his father's fellahin.
  |
  v
[THE ECONOMY TEST] -- checked on yearly pulse
  Is Tarek's factory profitable?
  (Check: industrial building throughput in his state, GDP growth, trade)
  |
  +-- YES --------> [THRIVING PATH]
  |
  +-- NO ---------> [CRISIS EVENT]
                       Player decision:
                       +-- "Subsidize" --> [RESCUED PATH]
                       +-- "Market decides" --> [FALLING PATH]
```

### THRIVING PATH

```
[TAREK THRIVES]
  Builds a second factory. Gets richer.
  |
  v
[WORKERS DEMAND RIGHTS] -- triggered by labor movement or IG pressure
  |
  +-- "Negotiate" --------> [FAIR MASTER BRANCH]
  |     Reluctantly improves conditions. Loyalty boost among laborers.
  |     Profits dip. He sleeps better.
  |     |
  |     v
  |   [TAREK THE PATRIARCH]
  |     Becomes what his father was -- paternalistic, in a factory.
  |     Knows every worker's name. Pays fairly.
  |     Personality shifts: interest_labor 8 -> 4.
  |     IG industrialists lose small clout, turmoil drops.
  |
  +-- "Market conditions" --> [RUTHLESS MASTER BRANCH]
        Longer hours, lower tolerance. Throughput bonus, radicals rise.
        |
        v
      [THE STRIKE] -- connects to Samier if active
        |
        +-- "Send police" --> [TAREK WINS, WORKERS LOSE]
        |     Radical spike, turmoil, factory resumes.
        |     Paranoid, hires private guards, rich but afraid.
        |
        +-- "Force negotiation" --> [TAREK BENDS]
              Throughput loss, loyalist boost.
              Hates it. Compromises. Grudging respect from workers.
              Still ambitious but humbled.
```

### FALLING PATH

```
[TAREK'S FACTORY FAILS]
  Sells at a loss. Debts pile up.
  |
  v
[THE FALL] -- life decision
  |
  +-- "Find work where he can" -----> [FACTORY FLOOR BRANCH]
  |     Pop type: Capitalist -> Laborer
  |     Home state: stays Cairo
  |     IG: Industrialists -> Trade Unions (potentially)
  |     Personality: interest_labor 8 -> 2 (he IS labor now)
  |     Small radical boost -- fallen capitalist is angry.
  |     |
  |     v
  |   [TAREK ON THE FACTORY FLOOR]
  |     Works the machines he used to own. The foreman doesn't know.
  |     His hands bleed. He thinks about his father's serfs.
  |     |
  |     v
  |   [TAREK AND SAMIER] -- if Samier active same state
  |     See crossings.md
  |
  +-- "Return to the land" -----> [RETURN TO FAYOUM BRANCH]
  |     Pop type: Capitalist -> Farmer
  |     Home state: Cairo -> Fayoum
  |     IG: Industrialists -> Rural Folk
  |     Works small remnant of family land. Terrible at farming.
  |     But the soil smells like his childhood.
  |     |
  |     v
  |   [TAREK THE FARMER]
  |     Harvest-condition events now fire for him. Humbled.
  |     Becomes what his father was before the title.
  |     |
  |     v
  |   [TAREK AND LAYLA] -- see crossings.md
  |
  +-- "Try again" -----> [SECOND CHANCE BRANCH]
        Borrows money. Smaller factory. Desperate, reckless.
        +-- Economy recovers: back to THRIVING but scarred.
        +-- Economy doesn't: loses everything. Falls to FACTORY FLOOR or FAYOUM.
```

### RESCUED PATH

```
[GOVERNMENT SUBSIDIZES TAREK]
  Treasury cost, factories don't close. Dependent on bureaucrats.
  Pride wounded. Becomes politically active -- lobbies, attends meetings.
  May become actual Executive role in National Cast.
  If player pulls support: falls to CRISIS again.
```

## Narrative Tone

Melancholic, complex. Tarek is not a villain. He is a man who grieved a world and then built a new one on top of its grave. The player should feel the weight of progress through him -- every factory built is someone's grandfather's tree cut down. He is proof that you can mourn the past and profit from the future at the same time, and that neither feeling cancels the other.
