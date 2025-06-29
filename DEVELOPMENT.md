# Exodia Assistant App - Developer Documentation

## Recent Changes
- **Tool configuration files** are now in **TOML** format instead of YAML. Update or add new role tools in TOML files (see `app/roles/profiles/<Role>/tools.toml`).
- The **Environment Setup tab** logic has been moved to `app/core/role_env_setup.py` for better modularity.
- The Environment tab UI now displays the **total number of tools and the number of installed tools** between the search bar and the Update Status button. This count updates live as you toggle tool checkboxes.

## Documentation Has Moved!

All developer and contributor documentation is now located in the `docs/` directory for easier navigation and maintenance.

## Quick Links
- [Overview & Quick Start](docs/index.md)
- [Project Structure](docs/structure.md)
- [Main Components](docs/components.md)
- [Development Environment Setup](docs/development.md)
- [Adding New Features & Roles](docs/features.md)
- [Styling Guidelines](docs/styling.md)
- [Contributing Guide](docs/contributing.md)
- [FAQ & Troubleshooting](docs/faq.md)

## How to Contribute
1. Read the [Contributing Guide](docs/contributing.md)
2. Set up your environment ([Development Setup](docs/development.md))
3. Explore the [Project Structure](docs/structure.md) and [Main Components](docs/components.md)
4. Add features or fix bugs as described in [Adding Features](docs/features.md)
5. Follow [Styling Guidelines](docs/styling.md) and test your changes
6. Submit a pull request!

---

For full details, see the `docs/` directory. Thank you for contributing to Exodia Assistant App!