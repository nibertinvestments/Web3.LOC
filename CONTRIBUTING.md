# Contributing to Web3.LOC

We love your input! We want to make contributing to Web3.LOC as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### 1. Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/your-username/Web3.LOC.git
cd Web3.LOC
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Changes

- Write clean, documented code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes

```bash
# Run tests
pytest

# Check code style
black --check .
flake8 .

# Test the application
streamlit run web3_loc_gui.py
```

### 6. Commit & Push

```bash
git add .
git commit -m "feat: add amazing new feature"
git push origin feature/your-feature-name
```

### 7. Create Pull Request

- Go to GitHub and create a pull request
- Fill out the PR template
- Link any related issues

## 📝 Pull Request Process

1. **Update documentation** for any new features
2. **Add tests** that cover your changes
3. **Ensure all tests pass** and code follows style guidelines
4. **Update the README.md** if you change functionality
5. **Request review** from maintainers

### PR Requirements

- [ ] Code follows the project's style guidelines
- [ ] Tests have been added for new functionality
- [ ] All tests pass
- [ ] Documentation has been updated
- [ ] PR description clearly describes changes

## 🐛 Bug Reports

Great bug reports tend to have:

- A quick summary and/or background
- Steps to reproduce (be specific!)
- What you expected would happen
- What actually happens
- Sample code (if applicable)
- Notes (possibly including why you think this might be happening)

### Bug Report Template

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
- OS: [e.g. Windows 10, macOS 12.0]
- Python Version: [e.g. 3.9.7]
- Web3.LOC Version: [e.g. 2.0.1]

**Additional Context**
Add any other context about the problem here.
```

## 💡 Feature Requests

We welcome feature requests! To suggest new features:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** you're trying to solve
3. **Explain your proposed solution**
4. **Consider alternative solutions**
5. **Provide use cases** and examples

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request.
```

## 🎨 Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Use absolute imports, group by standard/third-party/local
- **Naming**: Use descriptive names, snake_case for functions/variables
- **Documentation**: Use docstrings for all public functions/classes

### Code Formatting

We use [Black](https://black.readthedocs.io/) for automatic code formatting:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

### Linting

We use [Flake8](https://flake8.pycqa.org/) for linting:

```bash
# Run linter
flake8 .

# Configuration is in setup.cfg
```

### Pre-commit Hooks

Consider setting up pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_contract_analyzer.py

# Run with coverage
pytest --cov=contract_discovery
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_contract_analysis_with_valid_input`
- Mock external API calls
- Test both success and failure cases

### Test Structure

```python
import pytest
from contract_discovery.contract_analyzer import ContractAnalyzer

class TestContractAnalyzer:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.analyzer = ContractAnalyzer()
    
    def test_analyze_erc20_contract(self):
        """Test ERC20 contract analysis."""
        # Test implementation
        pass
    
    def test_analyze_invalid_contract(self):
        """Test error handling for invalid contracts."""
        # Test implementation
        pass
```

## 📚 Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Follow [Google docstring style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Include parameter types and return types
- Provide examples for complex functions

### Example Docstring

```python
def analyze_contract(self, contract_address: str, chain: str) -> Dict[str, Any]:
    """Analyze a smart contract and return classification data.
    
    Args:
        contract_address: The contract address to analyze
        chain: The blockchain network (ethereum, base, etc.)
        
    Returns:
        Dict containing contract analysis results including:
        - category: Contract category (ERC20, NFT, etc.)
        - security_score: Security analysis score (0-100)
        - features: List of detected features
        
    Raises:
        ValueError: If contract_address is invalid
        NetworkError: If blockchain network is unreachable
        
    Example:
        >>> analyzer = ContractAnalyzer()
        >>> result = analyzer.analyze_contract("0x123...", "ethereum")
        >>> print(result["category"])
        "ERC-20 Token"
    """
```

## 🏗️ Project Structure

Understanding the project structure helps with contributions:

```
Web3.LOC/
├── contract_discovery/           # Core discovery engine
│   ├── __init__.py
│   ├── blockchain_clients.py     # Blockchain API clients
│   ├── contract_database.py      # Database operations
│   ├── enhanced_blockchain_client.py
│   ├── github_storage.py         # GitHub integration
│   └── readme_generator.py       # Documentation generation
├── docs/                        # GitHub Pages website
│   ├── index.html
│   ├── css/
│   └── js/
├── tests/                       # Test files
├── .github/                     # GitHub workflows
├── requirements.txt            # Python dependencies
├── web3_loc_gui.py            # Streamlit interface
└── README.md                  # Project documentation
```

## 🚀 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **Major** (X.0.0): Breaking changes
- **Minor** (1.X.0): New features, backward compatible
- **Patch** (1.1.X): Bug fixes, backward compatible

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version number is bumped
- [ ] Changelog is updated
- [ ] Release notes are prepared

## 🤝 Community

### Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Be patient** with newcomers
- **Be mindful** of your words and actions

### Communication

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Reviews**: Provide constructive feedback on pull requests

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to Web3.LOC! 🚀