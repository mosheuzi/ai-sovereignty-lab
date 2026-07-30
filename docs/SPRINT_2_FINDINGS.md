# Sprint 2 Findings

## Main correction: TSMC Arizona

The current official TSMC Arizona page states a total planned United States investment of USD 165 billion. The v0.3 dataset contains USD 265 billion and must be corrected.

The current status should be represented as:

- First fab: operational, N4 high-volume production since Q4 2024
- Second fab: under development, N3 production targeted for the second half of 2027
- Third fab: under development, N2 and A16 targeted by the end of the decade
- Six fabs, two advanced-packaging facilities and an R&D center: overall plan, not current operational capacity

## Israel semiconductor capability is broader than Intel Israel

The Israel Innovation Authority's 2025 sector overview supports an aggregate national semiconductor node:

- Approximately 45,000 workers
- Approximately 200 companies
- Approximately 75 percent of workers in chip design
- Approximately 16 percent in metrology and inspection
- Two fabs identified in Israel, Tower in Migdal HaEmek and Intel in Kiryat Gat

This requires three separate national capabilities in the visual model:

1. Chip design
2. Metrology and inspection
3. Fabrication

They must not be collapsed into a single `semiconductor` status.

## Chips JU is allied access, not sovereignty

Israel's 2026 participation in the European Chips Joint Undertaking is an important capability. It provides access to joint R&D programs, European partners and public funding.

It should be visualized as:

`Israel -> allied research and funding access -> European semiconductor ecosystem`

It should not be visualized as domestic fabrication or control of the European supply chain.

## Israel's gas position is both a strength and a vulnerability

The State Comptroller supports a more nuanced energy node:

- More than 70 percent of electricity was generated using natural gas in 2024
- Israel had no natural-gas storage capacity at the time of the audit
- 49 percent of 2024 production was exported
- The audit warns of possible reserve depletion in approximately 25 years

Therefore the map should not show `Israel has gas` as equivalent to energy sovereignty.

A better representation is:

`Domestic gas resource -> electricity generation -> grid and data centers`

with visible resilience constraints for storage, long-term reserves, grid connection, generation redundancy and water or cooling requirements.

## INSS source supplied by the project owner

The supplied INSS URL is valuable for the strategic narrative and policy questions. Automated retrieval was blocked, so the exact page still requires manual inspection.

Related accessible INSS publications support the following analytical framing:

- Israel is strong in semiconductor R&D and design
- Semiconductor supply chains are global and geopolitically exposed
- Israel should examine a national semiconductor strategy and allied technology partnerships

However, INSS is a secondary analytical source. An accessible 2022 INSS article also refers to Intel's proposed Tower Semiconductor acquisition as though it had occurred. The transaction was terminated in August 2023. This confirms that INSS should not be used as the final source for current ownership or operational metrics.

## United States infrastructure status

### Intel

The final Intel CHIPS Act summary supports up to USD 7.86 billion in direct funding for projects in Arizona, New Mexico, Ohio and Oregon, within broader company plans exceeding USD 100 billion.

The dataset should distinguish:

- Final public funding award
- Company investment plan
- Existing operational sites
- New or expanded capacity still under construction

### Micron

Micron's approximately USD 200 billion United States plan is verified, but advanced HBM packaging remains planned. The interface must not render it as an operational domestic HBM capability.

### Data-center electricity

The United States Department of Energy supports:

- 4.4 percent of United States electricity in 2023
- 176 TWh in 2023
- 6.7 to 12 percent forecast for 2028
- 325 to 580 TWh forecast for 2028

The 2028 figures must be visually marked as forecasts.

## Schema finding

The status `domestically_owned` is too strong for many private companies.

The next dataset version should separate:

- Company origin
- Headquarters
- Operating locations
- Verified control country
- Ownership verification status

This is especially important for AI21 and other venture-backed companies with international investors and potentially cross-border corporate structures.

## Next research priorities

1. Manual review of the exact INSS page supplied by the project owner
2. Stable official text of Government Decision 4255
3. Primary-source review of Tower Semiconductor's Israeli fabrication operations
4. Israel electricity grid capacity and data-center connection constraints
5. Water, cooling and backup-generation requirements for Israeli AI data centers
6. Rebuild of canonical dataset v0.4 after review of the proposed patch plan
