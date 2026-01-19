---
name: code-review
description: Comprehensive code review with best practices, security, and maintainability checks. Use when reviewing pull requests, pre-commit code checks, learning code review techniques, improving code quality, or performing security audits. Triggers include "code review", "review code", "PR review", "pull request review", "security review", "code quality", or when evaluating code for issues and improvements.
---

# Code Review Skill

Comprehensive code review with best practices, security, and maintainability checks.

## Overview

This skill guides Claude through systematic code review, covering:
- Code quality and style
- Security vulnerabilities
- Performance considerations
- Best practices adherence
- Documentation quality
- Test coverage

## When to Use

- Reviewing pull requests
- Pre-commit code checks
- Learning code review techniques
- Improving code quality
- Security audits

## Prerequisites

- Basic understanding of the programming language being reviewed
- Familiarity with common security vulnerabilities (OWASP Top 10)
- Knowledge of language-specific best practices

## Instructions

### Review Process

1. **Initial Scan**
   - Understand the purpose of the code
   - Identify the programming language and framework
   - Note the scope and complexity

2. **Functional Review**
   - Does the code do what it's supposed to do?
   - Are edge cases handled?
   - Is error handling appropriate?

3. **Code Quality**
   - Is the code readable and maintainable?
   - Are variable/function names descriptive?
   - Is the code properly structured?
   - Are there code smells?

4. **Security Check**
   - SQL injection vulnerabilities
   - XSS (Cross-Site Scripting) risks
   - Authentication/authorization issues
   - Sensitive data exposure
   - Input validation

5. **Performance**
   - Algorithm efficiency
   - Database query optimization
   - Unnecessary computations
   - Memory leaks

6. **Best Practices**
   - Language-specific conventions
   - Design patterns usage
   - SOLID principles
   - DRY (Don't Repeat Yourself)

### Review Checklist

**Functionality**
- [ ] Code achieves stated purpose
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] Input validation implemented

**Code Quality**
- [ ] Clear, descriptive naming
- [ ] Appropriate comments
- [ ] Consistent formatting
- [ ] No code duplication
- [ ] Functions are focused and single-purpose

**Security**
- [ ] No SQL injection vulnerabilities
- [ ] User input sanitized
- [ ] Authentication properly implemented
- [ ] Sensitive data protected
- [ ] HTTPS enforced where needed

**Performance**
- [ ] Efficient algorithms
- [ ] No N+1 query problems
- [ ] Appropriate caching
- [ ] Resource cleanup

**Testing**
- [ ] Unit tests present
- [ ] Test coverage adequate
- [ ] Edge cases tested
- [ ] Integration tests if needed

**Documentation**
- [ ] Function/method documentation
- [ ] Complex logic explained
- [ ] API documentation
- [ ] README updated if needed

## Examples

### Example 1: Python Function Review

**Code:**
```python
def get_user(id):
    query = f"SELECT * FROM users WHERE id = {id}"
    result = db.execute(query)
    return result[0]
```

**Review:**

**🔴 Critical Issues:**
1. **SQL Injection Vulnerability**: Using string formatting for SQL query allows injection attacks
2. **No Error Handling**: Assumes query succeeds and returns results
3. **Index Out of Range**: No check if result is empty

**🟡 Suggestions:**
1. **Type Hints Missing**: Add type hints for parameters and return value
2. **Function Name**: Could be more specific (e.g., `get_user_by_id`)

**✅ Fixed Version:**
```python
from typing import Optional, Dict, Any

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user by their ID.
    
    Args:
        user_id: The unique identifier for the user
        
    Returns:
        User data as dictionary, or None if not found
    """
    query = "SELECT * FROM users WHERE id = %s"
    result = db.execute(query, (user_id,))
    return result[0] if result else None
```

### Example 2: React Component Review

**Code:**
```jsx
function UserList() {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);
  
  return (
    <div>
      {users.map(user => <div>{user.name}</div>)}
    </div>
  );
}
```

**Review:**

**🟡 Issues:**
1. **Missing Key Prop**: Map items need unique keys
2. **No Error Handling**: Fetch could fail
3. **No Loading State**: User sees nothing while loading
4. **Memory Leak Risk**: No cleanup if component unmounts during fetch

**Suggestions:**
1. Add loading and error states
2. Implement proper error handling
3. Add abort controller for fetch cleanup
4. Add unique keys to mapped elements

**✅ Improved Version:**
```jsx
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const abortController = new AbortController();
    
    fetch('/api/users', { signal: abortController.signal })
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch users');
        return res.json();
      })
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          setError(err.message);
          setLoading(false);
        }
      });
    
    return () => abortController.abort();
  }, []);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

## Common Pitfalls

### Over-Engineering
Don't suggest complex solutions for simple problems. Prefer clarity over cleverness.

### Language Assumptions
Verify language-specific best practices before making suggestions.

### Context Missing
Ask for additional context if needed (e.g., "What's the expected input range?")

### Tone
Be constructive and educational. Explain *why* something is an issue, not just *what* is wrong.

## Output Format

Structure reviews as:

```
## Summary
[Brief overview of findings]

## Critical Issues 🔴
[Security vulnerabilities, bugs, major problems]

## Important Issues 🟡
[Code quality, performance, maintainability]

## Suggestions 🟢
[Nice-to-haves, style improvements, optional enhancements]

## Positive Aspects ✨
[What's done well - always include this!]

## Overall Assessment
[Brief conclusion and recommendation]
```

## Limitations

- Can't execute code to verify functionality
- May miss context-specific business logic issues
- Can't verify integration with external systems
- Security review is not a substitute for professional audit

## Related Skills

- Security Audit (more focused security review)
- Performance Optimization (detailed performance analysis)
- Refactoring Guide (code improvement strategies)

## Author

Claude Toolkit Community

## Version

- **Created**: 2025-01-18
- **Last Updated**: 2025-01-18
- **Version**: 1.0.0
