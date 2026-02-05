# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in the AI Resume Analyzer, please report it responsibly:

1. **Email**: Send details to the project maintainer
2. **GitHub**: Use the private vulnerability reporting feature
3. **Do not** create public GitHub issues for security vulnerabilities

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Security Measures

### Data Privacy
- **No data storage**: Resume content is processed in memory only
- **No tracking**: No personal information is collected or stored
- **Session-based**: All data is discarded after analysis
- **Local processing**: Analysis runs locally or on your deployment

### Input Validation
- File type validation (PDF, DOCX, TXT only)
- File size limits (5MB maximum)
- Content sanitization to prevent injection attacks
- Input length restrictions to prevent DoS attacks

### API Security
- Rate limiting to prevent abuse
- Request timeout protection
- Input validation on all endpoints
- Error messages that don't leak system information
- CORS protection for web deployment

### Infrastructure Security
- Container security best practices
- Non-root user execution
- Minimal attack surface
- Regular dependency updates
- Secure default configurations

## Known Limitations

1. **File Processing**: Large files may consume significant memory
2. **PDF Parsing**: Complex PDFs might not extract text properly
3. **Rate Limiting**: API requests are limited to prevent abuse

## Best Practices for Users

1. **Local Deployment**: For sensitive resumes, deploy locally
2. **File Validation**: Only upload files you trust
3. **Environment Security**: Keep your deployment environment updated
4. **Access Control**: Restrict access to your deployment if needed

## Development Security

### Dependencies
- All dependencies are pinned to specific versions
- Regular security audits using tools like `pip-audit`
- Automated dependency updates with security patches

### Code Security
- Input validation on all user inputs
- Safe file handling practices
- No eval() or exec() usage
- Secure configuration management

## Reporting Issues

For non-security issues:
- GitHub Issues: Create a new issue with details
- Discussions: Use GitHub Discussions for questions
- Pull Requests: Submit fixes with proper testing

## Disclaimer

This tool is provided "as is" without warranty. Users are responsible for:
- Securing their deployment environment
- Protecting sensitive resume data
- Following applicable data privacy laws
- Regular security updates

## Updates

This security policy is updated with each major release. Check back regularly for updates.