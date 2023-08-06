# filedgr-nft-protobuf-python

This package wraps the serialization and deserialization of a Filedgr NFT URI. The protobuf package is used to allow a basic versioning from the beginning, and errorless multi-platform serialization/deserilaization.

The fields encoded in the NFT URI are:
- The NFT ID, which should be unique as per convention it will be complemented by a range of technical utility tokens. These can include transaction tokens for NFT updates and Access tokens for token gating.
- The Campaign ID: A unique ID for a NFT campaign, or user of suctomer.
- The NFT URI: as in other NFTs the link to actual object of the NFT.

