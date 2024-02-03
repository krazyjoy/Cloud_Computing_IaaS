class config:
    config_values ={
        "AWS_ACCESS_KEY_ID": "AKIASZJRVG7HNLD2E6IY",
        "AWS_SECRET_ACCESS_KEY": "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"
    }
    @classmethod
    def get_config(cls, key):
        if key in cls.config_values:
            return cls.config_values[key]
        else:
            raise ValueError(f"Configuration key '{key}' not found.")


class security_group_config:
    security_group_values={
        "CSE546_EC2_Security_Group": "sg-0a44fc06f53b1c1be"
    }

    @classmethod
    def get_security_group_config(cls, name):
        if name in cls.security_group_values:
            return cls.security_group_values[name]
        else:
            raise ValueError(f"Security Group Name $'{name}' not found.")