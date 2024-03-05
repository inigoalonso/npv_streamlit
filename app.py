import pandas as pd
import numpy as np
import numpy_financial as npf
import streamlit as st
import plotly.express as px


try:
    st.set_page_config(
        page_title="Net Present Value Calculator",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except:
    pass


def main():

    ###########################################################################
    # Sidebar
    ###########################################################################

    with st.sidebar:
        with st.form("inputs_form"):
            st.markdown("## Inputs")
            currency = st.selectbox(
                "Currency",
                options=["USD", "EUR", "GBP", "JPY", "CNY"],
            )
            time_horizon_years = st.number_input(
                "Time Horizon (Years)",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
            )
            rate = st.number_input(
                "Discount Rate",
                min_value=0.01,
                max_value=0.99,
                value=0.08,
                step=0.01,
                format="%.2f",
            )
            initial_investment = st.number_input(
                "Initial Investment",
                min_value=0,
                value=1000,
                step=100,
            )
            unit_cost = st.number_input(
                "Unit Cost",
                min_value=10,
                max_value=10000,
                value=500,
                step=10,
            )
            unit_price = st.number_input(
                "Unit Price",
                min_value=10,
                max_value=10000,
                value=1000,
                step=10,
            )
            cost_flow_type = st.selectbox(
                "Cost Flow Type",
                options=["Linear", "Exponential", "Logarithmic", "Sigmoidal"],
            )
            cost_flow_all_starting = st.number_input(
                "Cost Flow Starting Point",
                min_value=1,
                max_value=1000000,
                value=1000,
                step=1,
            )
            cost_flow_linear_slope = st.number_input(
                "Cost Flow Linear Slope",
                min_value=0.01,
                max_value=0.99,
                value=0.5,
                step=0.01,
                format="%.2f",
            )
            cost_flow_exponential_rate = st.number_input(
                "Cost Flow Exponential Rate",
                min_value=0.01,
                max_value=0.99,
                value=0.5,
                step=0.01,
                format="%.2f",
            )
            cost_flow_logarithmic_base = st.number_input(
                "Cost Flow Logarithmic Base",
                min_value=1,
                max_value=1000000,
                value=1000,
                step=1,
            )
            cost_flow_sigmoidal_carrying_capacity = st.number_input(
                "Cost Flow Sigmoidal Carrying Capacity",
                min_value=1,
                max_value=1000000,
                value=1000,
                step=1,
            )
            cost_flow_sigmoidal_rate = st.number_input(
                "Cost Flow Sigmoidal Rate",
                min_value=0.01,
                max_value=0.99,
                value=0.5,
                step=0.01,
                format="%.2f",
            )
            cost_flow_sigmoidal_inflection_point = st.number_input(
                "Cost Flow Sigmoidal Inflection Point",
                min_value=1,
                max_value=100,
                value=5,
                step=1,
            )
            revenue_flow_type = st.selectbox(
                "Revenue Flow Type",
                options=["Linear", "Exponential", "Logarithmic", "Sigmoidal"],
            )

            years = [year for year in range(time_horizon_years)]

            # fixed_cost = 100
            # fixed_revenue = 200
            # costs = [fixed_cost for _ in range(time_horizon_years)]
            # if len(costs) > 0:
            #     costs[0] = initial_investment
            # revenues = [fixed_revenue for _ in range(time_horizon_years)]
            if cost_flow_type == "Linear":
                costs = [
                    unit_cost * (cost_flow_all_starting + cost_flow_linear_slope * year)
                    for year in range(time_horizon_years)
                ]
            elif cost_flow_type == "Exponential":
                costs = [
                    unit_cost * (cost_flow_all_starting * cost_flow_exponential_rate**year)
                    for year in range(time_horizon_years)
                ]
            elif cost_flow_type == "Logarithmic":
                costs = [
                    unit_cost * (cost_flow_all_starting
                    + cost_flow_logarithmic_base* np.log(year + 1))
                    for year in range(time_horizon_years)
                ]
            elif cost_flow_type == "Sigmoidal":
                costs = [
                    unit_cost * (cost_flow_all_starting
                    + cost_flow_sigmoidal_carrying_capacity
                    * (
                        1
                        - (
                            1
                            / (
                                1
                                + cost_flow_sigmoidal_rate
                                ** (year - cost_flow_sigmoidal_inflection_point)
                            )
                        )
                    ))
                    for year in range(time_horizon_years)
                ]
            if len(costs) > 0:
                costs[0] = initial_investment
            if revenue_flow_type == "Linear":
                revenues = [unit_price * year for year in range(time_horizon_years)]
            elif revenue_flow_type == "Exponential":
                revenues = [unit_price * 2**year for year in range(time_horizon_years)]
            elif revenue_flow_type == "Logarithmic":
                revenues = [
                    unit_price * (year + 1) for year in range(time_horizon_years)
                ]
            elif revenue_flow_type == "Sigmoidal":
                revenues = [
                    unit_price * (1 - (1 / (1 + 2 ** (year - 5))))
                    for year in range(time_horizon_years)
                ]

            cash_flows = [revenue - cost for revenue, cost in zip(revenues, costs)]
            discounted_cash_flows = [
                cash_flow / (1 + rate) ** year
                for year, cash_flow in enumerate(cash_flows)
            ]
            cumulative_costs = [
                sum(costs[: year + 1]) for year in range(time_horizon_years)
            ]
            cumulative_revenues = [
                sum(revenues[: year + 1]) for year in range(time_horizon_years)
            ]
            cumulative_cash_flows = [
                sum(cash_flows[: year + 1]) for year in range(time_horizon_years)
            ]
            cumulative_discounted_cash_flows = [
                sum(discounted_cash_flows[: year + 1])
                for year in range(time_horizon_years)
            ]
            total_cost = sum(costs)
            total_revenue = sum(revenues)
            total_cash_flow = sum(cash_flows)
            npv = npf.npv(rate, cash_flows)
            irr = npf.irr(cash_flows)
            df = pd.DataFrame(
                {
                    "Year": years,
                    "Cost": costs,
                    "Revenue": revenues,
                    "Cash Flow": cash_flows,
                    "Discounted Cash Flow": discounted_cash_flows,
                    "Cumulative Cost": cumulative_costs,
                    "Cumulative Revenue": cumulative_revenues,
                    "Cumulative Cash Flow": cumulative_cash_flows,
                    "Cumulative Discounted Cash Flow": cumulative_discounted_cash_flows,
                }
            )

            st.form_submit_button(
                "Update calculations",
                help="Click to update the calculations",
                use_container_width=True,
            )

    ###########################################################################
    # Main App
    ###########################################################################

    st.title("Net Present Value Calculator")

    if time_horizon_years == 0:
        st.warning("Adjust the inputs in the sidebar to see how the NPV changes.")
    else:
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

        with col1:
            st.metric(
                label="Total Cost",
                value=f"{total_cost:.2f}",
            )

        with col2:
            st.metric(
                label="Total Revenue",
                value=f"{total_revenue:.2f}",
            )

        with col3:
            st.metric(
                label="Total Cash Flow",
                value=f"{total_cash_flow:.2f}",
            )

        with col4:
            st.metric(
                label="Internal Rate of Return (IRR)",
                value=f"{irr:.2%}",
            )

        with col5:
            st.metric(
                label="Net Present Value (NPV)",
                value=f"{npv:.2f}",
            )

        fig = px.line(
            pd.DataFrame(
                {
                    "Year": years,
                    "Cost": costs,
                    "Revenue": revenues,
                    "Cash Flow": cash_flows,
                    "Discounted Cash Flow": discounted_cash_flows,
                    "Cumulative Cost": cumulative_costs,
                    "Cumulative Revenue": cumulative_revenues,
                    "Cumulative Cash Flow": cumulative_cash_flows,
                    "Cumulative Discounted Cash Flow": cumulative_discounted_cash_flows,
                }
            ),
            x="Year",
            y=[
                "Cost",
                "Revenue",
                "Cash Flow",
                "Discounted Cash Flow",
                "Cumulative Cost",
                "Cumulative Revenue",
                "Cumulative Cash Flow",
                "Cumulative Discounted Cash Flow",
            ],
            labels={"x": "Year", "value": currency},
            title="Costs, Revenues, and Cash Flows Over Time",
        ).update_traces(
            visible="legendonly",
            selector=lambda t: not t.name
            in ["Cost", "Revenue", "Cash Flow", "Cumulative Discounted Cash Flow"],
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander(
            "Data Table",
            expanded=False,
        ):
            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True,
            )

        with st.expander(
            "Additional inputs",
            expanded=False,
        ):
            col1_addditional, col2_addditional, col3_addditional, col4_addditional = st.columns(
                [1, 1, 1, 1]
            )
            with col1_addditional:
                st.markdown("#### Linear cost flow")
                st.write(
                    f"Cost Flow Starting Point: {cost_flow_all_starting}"
                )
                st.markdown("#### Linear revenue flow")
            
            with col2_addditional:
                st.markdown("#### Exponential cost flow")

                st.markdown("#### Exponential revenue flow")

            with col3_addditional:
                st.markdown("#### Logarithmic cost flow")

                st.markdown("#### Logarithmic revenue flow")

            with col4_addditional:
                st.markdown("#### Sigmoidal cost flow")

                st.markdown("#### Sigmoidal revenue flow")


        with st.expander(
            "Definitions",
            expanded=False,
        ):
            st.write(
                """
                - **Discount Rate**: The rate used to discount future cash flows.
                - **Time Horizon**: The number of years over which the project is evaluated.
                - **Initial Investment**: The amount of money invested at the beginning of the project.
                - **Unit Cost**: The cost of producing a single unit.
                - **Unit Price**: The price at which a single unit is sold.
                - **Cost Flow Type**: The type of cost flow over time.
                - **Revenue Flow Type**: The type of revenue flow over time.
                - **NPV**: The net present value of the project.
                - **IRR**: The internal rate of return of the project.
                - **Cumulative Cost**: The total cost over time.
                - **Cumulative Revenue**: The total revenue over time.
                - **Cumulative Cash Flow**: The total cash flow over time.
                - **Cumulative Discounted Cash Flow**: The total discounted cash flow over time.
                - **Costs**: The costs over time.
                - **Revenues**: The revenues over time.
                - **Cash Flows**: The cash flows over time.
                - **Discounted Cash Flows**: The discounted cash flows over time.
                - **Years**: The years over which the project is evaluated.
                - **Currency**: The currency used to display the values.
                - **Total Cost**: The total cost of the project.
                - **Total Revenue**: The total revenue of the project.
                - **Total Cash Flow**: The total cash flow of the project.
                - **Cost Flow Starting Point**: The starting point of the cost flow.
                - **Cost Flow Linear Slope**: The slope of the linear cost flow.
                - **Cost Flow Exponential Rate**: The rate of the exponential cost flow.
                - **Cost Flow Logarithmic Base**: The base of the logarithmic cost flow.
                - **Cost Flow Sigmoidal Carrying Capacity**: The carrying capacity of the sigmoidal cost flow.
                - **Cost Flow Sigmoidal Rate**: The rate of the sigmoidal cost flow.
                - **Cost Flow Sigmoidal Inflection Point**: The inflection point of the sigmoidal cost flow.
                """
            )


if __name__ == "__main__":
    main()
