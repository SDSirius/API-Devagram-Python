import boto3
from botocore.exceptions import ClientError
from decouple import config


class AWSProvider:
    def upload_arquivo_s3(self, caminho_para_salvar, caminho_do_arquivo, bucket='devaria-teste'):

        s3_client = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCES_KEY'),
            aws_secret_access_key=config('AWS_SECRET_KEY')
        )

        try:
            url = s3_client.generate_presigned_url(
                "get_object",
                ExpiresIn=0,
                Params={"Bucket": bucket, 'Key': caminho_para_salvar}
            )
            url = url.split('?')[0]
            print(url)
            return url

        except ClientError as erro:
            print(f'Erro dentro do AWSProvider ->  {erro}')
            return False
