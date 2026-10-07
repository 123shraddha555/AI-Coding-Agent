import streamlit as st

from agent import create_client, analyze_task, generate_changes
from codebase import build_codebase_context
from validator import validate_proposed_changes
from diff_generator import generate_diff


# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Coding Agent",
    page_icon="🤖",
    layout="wide"
)


# SESSION STATE
 
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "changes" not in st.session_state:
    st.session_state.changes = None


# HEADER

st.title("AI Coding Agent")

st.write(
    "An AI-powered coding agent that analyzes a codebase, "
    "identifies relevant files, proposes code changes, "
    "shows a diff, and validates the proposed changes."
)


# AGENT SETTINGS

st.sidebar.header("Agent Settings")

st.sidebar.info(
    "This application uses Gemini as the AI coding agent."
)


# GEMINI API KEY

api_key = st.secrets.get("GEMINI_API_KEY")


# DEVELOPER TASK
task = st.text_area(
    "Developer Task",
    value=(
        "Add email validation to the user registration API "
        "and write a test for invalid emails."
    ),
    height=120
)


# =========================================================
# ANALYZE TASK
# =========================================================

if st.button(
    "Analyze Task",
    use_container_width=True
):

    if not api_key:
        st.error(
            "Please enter your Gemini API key."
        )
        st.stop()

    if not task.strip():
        st.error(
            "Please enter a developer task."
        )
        st.stop()

    try:

        with st.spinner(
            "Reading codebase and analyzing task..."
        ):

            codebase_path = "sample_project"

            codebase_context = build_codebase_context(
                codebase_path
            )

            client = create_client(
                api_key
            )

            analysis = analyze_task(
                client,
                task,
                codebase_context
            )

            st.session_state.analysis = analysis

        st.success(
            "Task analyzed successfully."
        )

    except RuntimeError as error:

        st.error(
            str(error)
        )

    except Exception as error:

        st.error(
            f"Could not analyze task: {error}"
        )


# DISPLAY ANALYSIS


if st.session_state.analysis:

    st.subheader(
        "Agent Analysis"
    )

    st.markdown(
        st.session_state.analysis
    )


# PROPOSE CODE CHANGES

if st.button(
    "Propose Code Changes",
    use_container_width=True
):

    if not api_key:
        st.error(
            "Please enter your Gemini API key."
        )
        st.stop()

    if not task.strip():
        st.error(
            "Please enter a developer task."
        )
        st.stop()

    try:

        with st.spinner(
            "Generating proposed code changes..."
        ):

            codebase_path = "sample_project"

            codebase_context = build_codebase_context(
                codebase_path
            )

            client = create_client(
                api_key
            )

            changes = generate_changes(
                client,
                task,
                codebase_context
            )

            st.session_state.changes = changes

        st.success(
            "Code changes generated successfully."
        )

    except RuntimeError as error:

        st.error(
            str(error)
        )

        st.stop()

    except Exception as error:

        st.error(
            f"Could not generate changes: {error}"
        )

        st.stop()



# DISPLAY PROPOSED CHANGES
if st.session_state.changes:

    changes = st.session_state.changes

    st.subheader(
        "Proposed Changes"
    )

    st.write(
        changes["explanation"]
    )

    for change in changes["changes"]:

        file_path = change["file"]

        updated_code = change["updated_code"]

        st.markdown(
            f"### `{file_path}`"
        )

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                original_code = file.read()

            diff = generate_diff(
                original_code,
                updated_code,
                file_path
            )

            if diff:

                st.code(
                    diff,
                    language="diff"
                )

            else:

                st.info(
                    "No changes detected."
                )

        except FileNotFoundError:

            st.error(
                f"File not found: {file_path}"
            )


# VALIDATION
st.divider()

st.subheader(
    "Project Validation"
)

st.write(
    "Apply the proposed changes to a temporary copy "
    "of the project and run the pytest test suite. "
    "The original project files will not be modified."
)


if st.button(
    "Validate Proposed Changes",
    use_container_width=True
):

    if not st.session_state.changes:

        st.warning(
            "Please generate proposed code changes first."
        )

        st.stop()

    with st.spinner(
        "Applying proposed changes and running tests..."
    ):

        result = validate_proposed_changes(
            st.session_state.changes["changes"]
        )

    if result["success"]:

        st.success(
            "Proposed changes passed all tests."
        )

    else:

        st.error(
            "Proposed changes failed validation."
        )

    st.code(
        result["output"]
    )


# FOOTER
st.divider()

st.caption(
    "AI Coding Agent — Gemini-powered repository analysis, "
    "code change proposal, diff generation, and validation."
)