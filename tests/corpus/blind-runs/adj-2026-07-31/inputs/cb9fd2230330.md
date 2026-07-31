---
id: adrs-adr002
title: 'ADR002: Default Software Catalog File Format'
description: Architecture Decision Record (ADR) log on Default Software Catalog File Format
---

## Format

Descriptor files use the [YAML](https://yaml.org/spec/1.2/spec.html) format.
They may be written by hand or created using automated tools. Each file may
consist of several YAML documents (separated by `---`), where each document
describes a single entity.

This is an example entity definition with some mocked data.

```yaml
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: frobs-awesome
  description: |
    Backend service that implements the Frobs API, as defined
    in [the Frobs RFC](https://example.com/spec/frob.html).
  labels:
    system: frobs
    lifecycle: production
    example.com/service-discovery-name: frobsawesome
  annotations:
    circleci.com/project-slug: github/example-org/frobs-awesome
spec:
  type: service
```

The root fields `apiVersion`, `kind`, `metadata`, and `spec` are part of the
_envelope_, defining the overall structure of all kinds of entities. Likewise, the
`name`, `namespace`, `labels`, and `annotations` metadata fields are of special
significance and have reserved purposes and distinct shapes.

See below for details about these fields.

## Envelope

The root envelope object has the following structure.

### `apiVersion` and `kind`

The `kind` is the high level entity type being described, typically from the
[Backstage system model](https://github.com/backstage/backstage/issues/390). The
first versions of the catalog will focus on the `Component` kind.

The `apiVersion` is the version of the specification format for that particular
entity that this file is written against. The version is used for being able to
evolve the format, and the tuple of `apiVersion` and `kind` should be enough for
a parser to know how to interpret the contents of the rest of the document.

Backstage specific entities have an `apiVersion` that is prefixed with
`backstage.io/`, to distinguish them from other types of objects that share the
same type of structure. This may be relevant when co-hosting these
specifications with, e.g., Kubernetes object manifests.

Early versions of the catalog will be using alpha/beta versions, e.g.,
`backstage.io/v1alpha1` to signal that the format may still change. After that,
we will be using `backstage.io/v1` and up.

### `metadata`

A structure that contains metadata about the entity, i.e., things that aren't
directly part of the entity specification itself. See below for more details
about this structure.

### `spec`

The actual specification data that describes the entity.

The precise structure of the `spec` depends on the `apiVersion` and `kind`
combination, and some kinds may not even have a `spec` at all. See further down
in this document for the specification structure of specific kinds.

## Metadata

The `metadata` root field has the following nested structure.

### `name`

The name of the entity. This name is both meant for human eyes to recognize the
entity, and for machines and other components to reference the entity (e.g. in
URLs or from other entity specification files).

Names must be unique per kind, within a given namespace (if specified), at any
point in time. This uniqueness constraint is also case insensitive. Names may be
reused at a later time, after an entity is deleted from the registry.

Names are required to follow a certain format. Entities that do not follow those
rules will not be accepted for registration in the catalog. The ruleset is
configurable to fit your organization's needs, but the default behavior is as
follows.

- Strings of length at least 1, and at most 63
- Must consist of sequences of `[a-z0-9A-Z]` possibly separated by one of
  `[-_.]`

Example: `visits-tracking-service`, `CircleciBuildsDs_avro_gcs`

### `namespace`

The `name` of a namespace that the entity belongs to. This field is optional
and currently has no special semantics apart from bounding the name uniqueness
constraint if specified. It is reserved for future use and may get broader
semantic implication.

Namespaces may also be part of the catalog and are `v1` / `Namespace` entities,
i.e., not Backstage specific but the same as in Kubernetes.

### `description`

A human readable description of the entity to be shown in Backstage. Should be
kept short and informative, suitable to give an overview of the entity's purpose
at a glance. More detailed explanations and documentation should be placed
elsewhere.

### `labels`

Labels are optional key/value pairs that are attached to the entity, and
their use is identical to
[kubernetes object labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).

Their main purpose is for references to other entities and for information that
is in one way or another classifying for the current entity. They are often used
as values in queries or filters.

Both the key and the value are strings, subject to the following restrictions.

Keys have an optional prefix followed by a slash, and then the name part, which
is required. The prefix must be a valid lowercase domain name, at most 253
characters in total. The name part must be sequences of `[a-zA-Z0-9]` separated
by any of `[-_.]`, at most 63 characters in total.

The `backstage.io/` prefix is reserved for use by Backstage core components.
Some keys, such as `system` also have predefined semantics.

Values are strings that follow the same restrictions as `name` above.

### `annotations`

An object with arbitrary non-identifying metadata attached to the entity,
identical in use to
[kubernetes object annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/).

Their purpose is mainly, but not limited, to reference into external systems.
This could, for example, be a reference to the git ref the entity was ingested
from, to monitoring and logging systems, to pagerduty schedules, etc.

Both the key and the value are strings, subject to the following restrictions.

Keys have an optional prefix followed by a slash, and then the name part, which
is required. The prefix must be a valid lowercase domain name, at most 253
characters in total. The name part must be sequences of `[a-zA-Z0-9]` separated
by any of `[-_.]`, at most 63 characters in total.

The `backstage.io/` prefix is reserved for use by Backstage core components.

Values can be of any length but are limited to being strings.

## Component

| Field        | Value                   |
| ------------ | ----------------------- |
| `apiVersion` | `backstage.io/v1alpha1` |
| `kind`       | `Component`             |

The `spec` object for this kind is as follows:

| Field  | Type   | Required | Description                            |
| ------ | ------ | -------- | -------------------------------------- |
| `type` | String | Yes      | The type of component, e.g. `service`. |
