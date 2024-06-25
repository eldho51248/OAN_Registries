/** @odoo-module */
import {registry} from "@web/core/registry";
import {Component, useState, useSubEnv} from "@odoo/owl";
import {getDefaultConfig} from "@web/views/view";

export class G2PSupersetDashboard extends Component {




    async setup() {
        this.state = useState({
            isLoading: true,
            cookieService: null,
        });

        useSubEnv({
            config: {
                ...getDefaultConfig(),
                ...this.env.config,
            },
        });

        const orm = this.env.services.orm;
        this.getSupersertUrl(orm);
    }

    async getSupersertUrl(orm) {
        const data = await orm.searchRead(
            "ir.config_parameter",
            [["key", "=", "g2p_superset_dashboard.superset_url"]],
            ["value"]
        );

        if (data && data.length > 0 && data[0].value) {
            this.superSetUrl = data[0].value;
        } else {
            this.superSetUrl = false;
        }

        this.state.isLoading = false;
    }

    async attemptLogin() {
        try {
            console.log(`this is the url ${this.superSetUrl}/api/v1/security/login`);

            const response = await fetch(`${this.superSetUrl}/api/v1/security/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    password: "tr17",
                    provider: "db",
                    refresh: true,
                    username: "tr17",
                }),
                credentials: "include",
            });

            if (!response.ok) {
                throw new Error(`Login failed with status ${response.status}`);
            }

            console.log(`The login API request is successful here is status ${response.status}`);

            const data = await response.json();
            return {success: data.success};
        } catch (error) {
            console.error("Error during login:", error);
            return {success: false};
        }
    }
}

G2PSupersetDashboard.template = "g2p_superset_dashboard.G2PSupersetDashboard";
registry.category("actions").add("g2p.superset_dashboard", G2PSupersetDashboard);
