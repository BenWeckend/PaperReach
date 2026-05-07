## PaperReach/LitAgend (intelligent systems project)

scientific paper Research tool.

**Idea**: Paste entire Paragraphs into the tool and it will research and rate scientific Papers that match the given claim.

Workflow, Idea and Todos:
- Will be made in Python using Qt

1. Input Layer (User to System)
2. Core Layer
    - Query-Builder
    - Retrieval-Layer APIs:
        - Semantic Scholar API
        - arXiv API
        - CrossRef API
    - Relevance-Layer with "Claim-Matching"
    - (maybe some Citation Agend)
3. Output Layer with UI

Phase 0: Basic UI erstellen
Phase 1: Input → Keyword Search → Querys erzeugen
Phase 2: Papers durch die semanticscholar und arXiv API beziehen und als Liste anzeigen
Phase 3: Inhalt der Paper auslesen und im Bezug zum gegebenden Text bewerteten lassen.
Phase ... : Server backend aufsetzten das die API Anfragen macht und die Infos an den User weiterleitet. (So kann man den API Key nicht aus dem Binarydekompilieren)

Code Diagramm:
<img width="847" height="505" alt="code_diagram" src="https://github.com/user-attachments/assets/bf3495ce-c507-4ffa-88e1-b9324ed96fd8" />

Basic first Project Diagramm:
<img width="1321" height="1113" alt="Component_diagram" src="https://github.com/user-attachments/assets/52e2434f-23f2-4b7f-8776-3bb69c24fc18" />
[UML](/pr-docs/structure_and_planning/Component_diagram.plantuml)
