---
type: landing

sections:
  - block: collection
    content:
      title: Preprint
      filters:
        folders:
          - publication
        publication_type: 'article'
    design:
      view: citation
      css_class: pub-group

  - block: collection
    content:
      title: Journal article
      filters:
        folders:
          - publication
        publication_type: 'article-journal'
    design:
      view: citation
      css_class: pub-group

  - block: collection
    content:
      title: Conference papers
      filters:
        folders:
          - publication
        publication_type: 'paper-conference'
    design:
      view: citation
      css_class: pub-group

  - block: collection
    content:
      title: Thesis
      filters:
        folders:
          - publication
        publication_type: 'thesis'
    design:
      view: citation
      css_class: pub-group


cascade:
  reading_time: false
  share: false
  profile: false
  pager: false
---
