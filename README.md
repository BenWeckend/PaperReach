## PaperReach/LitAgend (intelligent systems project)

scientific paper Research tool.

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

Phase 1: Input → Keyword Search → Paper Liste anzeigen

Phase ... : Server backend aufsetzten das die API Anfragen macht und die Infos an den User weiterleitet. (So kann man den API Key nicht aus dem Binarydekompilieren)

- [x] PlantUML Structure

[UML](/pr-docs/structure_and_planning/Component_diagram.plantuml)

<img width="1321" height="1113" alt="Component_diagram" src="https://github.com/user-attachments/assets/52e2434f-23f2-4b7f-8776-3bb69c24fc18" />
