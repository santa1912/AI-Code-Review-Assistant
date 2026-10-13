import streamlit as st

from reviewer import review_code


st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 AI Code Review Assistant")
st.caption(
    "Review source code for potential bugs, security risks, "
    "readability, and maintainability."
)

st.info(
    "Prototype mode: without an API key, the app validates input "
    "but does not perform AI-powered analysis."
)

with st.form("review_form"):
    language = st.selectbox(
        "Programming language",
        ["Python", "JavaScript", "TypeScript", "Java", "C#", "Other"],
    )

    code = st.text_area(
        "Paste your code",
        height=300,
        placeholder="Paste your source code here...",
    )

    submitted = st.form_submit_button(
        "Review Code",
        type="primary",
    )

if submitted:
    try:
        with st.spinner("Reviewing code..."):
            result = review_code(code, language)

        st.divider()
        st.subheader("Review Summary")
        st.write(result["summary"])

        findings = result["findings"]
        st.subheader(f"Findings ({len(findings)})")

        if findings:
            for index, finding in enumerate(findings, start=1):
                severity = finding["severity"].strip().lower()
                title = finding["title"]
                line = finding["line"]
                description = finding["description"]

                with st.expander(f"{index}. {title}", expanded=True):
                    st.write(f"**Severity:** {severity.upper()}")
                    st.write(f"**Line:** {line}")
                    st.write(description)
        else:
            st.write("No findings to display.")

        st.caption(f"Characters submitted: {result['code_length']}")

    except (ValueError, TypeError) as exc:
        st.error(str(exc))
    except Exception:
        st.error(
            "The review could not be completed. "
            "Please check your configuration and try again."
        )