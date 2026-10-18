# Replica-skill note

The requested `Jakeschincariol/replica-skill` repository was reviewed as part
of this work. It is an MIT-licensed set of eleven Claude-oriented skills for a
clean-room sequence: recon → architecture → design → build → backend → test →
diff → brand → launch/deploy.

For Ruflo, the direct integration path is preferable to a reverse-engineered
clone because Ruflo itself is published under MIT. This bridge therefore:

- uses a fresh Muse Code skill that preserves the clean-room boundary for any
  future product-parity request;
- integrates the published Ruflo package through its documented local MCP
  command rather than copying its code or pretending to reproduce private
  behavior;
- records both upstream licenses and avoids carrying their source trees in this
  repository.

The `ruflo-replica-plan` command keeps the useful clean-room workflow: public,
authorized evidence; a scoped feature matrix; original code/assets/brand; and
measured rather than claimed parity.
