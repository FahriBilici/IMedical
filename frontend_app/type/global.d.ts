export {}
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID: string
      NEXT_PUBLIC_ALCHEMY_ID: string
      NEXT_PUBLIC_INPUT_BOX_ADDRESS: string
      NEXT_PUBLIC_DAPP_ADDRESS: string
      NEXT_PUBLIC_PROVIDER_URL: string
      NEXT_PUBLIC_GRAPHQL_ENDPOINT: string
    }
  }
}